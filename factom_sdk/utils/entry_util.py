import validators
import datetime
import factom_sdk.utils.consts
from factom_sdk.utils.key_util import KeyUtil
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


class EntryUtil:
    @staticmethod
    def get_entry_info(chain_id: str, entry_hash: str, signature_validation=None, request_handler=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        if not entry_hash:
            raise Exception("entry_hash is required.")
        response = request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                 factom_sdk.utils.consts.ENTRIES_URL, entry_hash]))
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            return {
                "entry": response,
                "status": ValidateSignatureUtil.validate_signature(response, False, request_handler)
            }
        elif callable(signature_validation):
            return {
                "entry": response,
                "status": signature_validation(response)
            }
        return response

    @staticmethod
    def create_entry(chain_id: str, automatic_signing: bool, content: str, external_ids: list = None,
                     signer_private_key: str = "", signer_chain_id: str = "", callback_url: str = "",
                     callback_stages=None, request_handler=None):
        if callback_stages is None:
            callback_stages = []
        if external_ids is None:
            external_ids = []
        if not chain_id:
            raise Exception("chain_id is required.")
        if automatic_signing:
            if not isinstance(external_ids, list):
                raise Exception("external_ids must be an array.")
            if not signer_private_key:
                raise Exception("signer_private_key is required.")
            if not KeyUtil.validate_checksum(signer_private_key):
                raise Exception("signer_private_key is invalid.")
            if not signer_chain_id:
                raise Exception("signer_chain_id is required.")
        else:
            if not external_ids:
                raise Exception("at least 1 external_id is required.")
            if not isinstance(external_ids, list):
                raise Exception("external_ids must be an array.")
            if signer_private_key and not signer_chain_id:
                raise Exception("signer_chain_id is required when passing a signer_private_key.")
            if signer_private_key and not KeyUtil.validate_checksum(signer_private_key):
                raise Exception("signer_private_key is invalid.")
            if signer_chain_id and not signer_private_key:
                raise Exception("signer_private_key is required when passing a signer_chain_id.")
        if not content:
            raise Exception("content is required.")
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        ids_base64 = []
        if automatic_signing:
            time_stamp = datetime.datetime.utcnow().isoformat()
            message = signer_chain_id + content + time_stamp
            signature = KeyUtil.sign_content(signer_private_key, message)
            signer_public_key = KeyUtil.get_public_key_from_private_key(signer_private_key)
            ids_base64.append(CommonUtil.base64_encode("SignedEntry"))
            ids_base64.append(CommonUtil.base64_encode(bytes([0x01])))
            ids_base64.append(CommonUtil.base64_encode(signer_chain_id))
            ids_base64.append(CommonUtil.base64_encode(signer_public_key))
            ids_base64.append(signature)
            ids_base64.append(CommonUtil.base64_encode(time_stamp))
        for val in external_ids:
            ids_base64.append(CommonUtil.base64_encode(val))
        data = {
            "external_ids": ids_base64,
            "content": CommonUtil.base64_encode(content)
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        return request_handler.post("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                              factom_sdk.utils.consts.ENTRIES_URL]), data)

    @staticmethod
    def get_entries(chain_id: str, limit: int = -1, offset: int = -1, stages: list = None, request_handler=None):
        if stages is None:
            stages = []
        if not chain_id:
            raise Exception("chain_id is required.")
        data = {}
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            data["limit"] = limit
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            data["offset"] = offset
        if not isinstance(stages, list):
            raise Exception("stages must be an array.")
        if stages:
            data["stages"] = ",".join(stages)
        return request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                             factom_sdk.utils.consts.ENTRIES_URL]), data)

    @staticmethod
    def get_first_entry(chain_id: str, request_handler=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        return request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                             factom_sdk.utils.consts.ENTRIES_URL, factom_sdk.utils.consts.FIRST_URL]))

    @staticmethod
    def get_last_entry(chain_id: str, request_handler=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        return request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                             factom_sdk.utils.consts.ENTRIES_URL, factom_sdk.utils.consts.LAST_URL]))

    @staticmethod
    def search_entries(chain_id: str, external_ids: list, limit: int = -1, offset: int = -1, request_handler=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        if not external_ids:
            raise Exception("at least 1 external_id is required.")
        if not isinstance(external_ids, list):
            raise Exception("external_ids must be an array.")
        url = "/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id, factom_sdk.utils.consts.ENTRIES_URL,
                        factom_sdk.utils.consts.SEARCH_URL])
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            url += "?limit=" + str(limit)
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            if limit > -1:
                url += "&offset=" + str(offset)
            else:
                url += "?offset=" + str(offset)
        ids_base64 = [CommonUtil.base64_encode(val) for val in external_ids]
        data = {"external_ids": ids_base64}
        return request_handler.post(url, data)
