identities
-----

An **Identity** contains 3 components: a names array, a set of currently active keys, and an auditable history of what other keys were active at a given point in time.

Each **Identity** uses their currently active keys to sign messages, proving that the messages came from the Identity. These messages are typically chains and entries that are written to the blockchain, but can be used off-chain as well for scenarios such as authentication.

The **Keys** for an **Identity** have priorities, where keys with a higher priority take precedence over those below them.

- Key priority is indicated by its index in the key array, i.e [“priority 1”, “priority 2”, “priority 3”].
- Keys can be replaced by those at the same or higher priority.
- The first key is the highest priority key for an Identity. Since it can be used to replace all other keys, it should be kept the most secure and used the least frequently to reduce the risk of it being mishandled or compromised. We recommend storing this key in “cold storage”.
- The lower priority keys are typically kept in “hot storage” and accessible for use by your live application. Still, these keys should be treated with care, for example: not being stored in repositories or not being stored in plaintext, etc. as they could be used by anyone, whom obtains them to indicate ownership of an Identity.

### Table of Contents

- [create](#identities_create)
- [get](#identities_get)
- [keys](#identities_keys)
	- [list](#keys_list)
	- [get](#keys_get)
	- [replace](#keys_replace)

### <a name="identities_create"></a>create

Creates a new Identity chain. You will need to include a unique names array for your Identity. This method will automatically generate 3 Public/Private keys pairs for you and return them, be sure to save them for future use. Optionally, you can pass in an array of public keys you have generated on your own, at which point no keys will be returned.

**Sample**
```python
 factom_client.identities.create(["NotarySimulation", "Test Identity"])
```

**Parameters**

| **Name**                | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | **SDK Error Message & Description**             <img width=2000/>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `names`          | required | array of strings </br> The names array for your identity must be unique. We recommend generating a unique identifier, such as a UUID. **Do NOT put personally identifiable information (PII) or your database records’ ID's on the blockchain.** </br> **Note:** Since the Connect API requires each array element to be Base64 encoded, the SDK will do so before making the API request.                                                                                                                                                                                                             | **at least 1 name is required.** </br> `names` parameter was not provided. </br></br>  **names must be an array.** </br> An invalid `names` format was provided.  </br> </br> **calculated bytes of names and keys is <*totalBytes*>. It must be less than 10240, use less/shorter names or less keys.** </br> Too many `names` or `keys` were provided resulting in calculated bytes being larger than 10kb.                                                                                                                                                                                                                                                                                                                      |
| `keys`           | optional | array of strings </br> An array of public key strings in base58 idpub format, ordered from the highest to the lowest priority. </br> **Note:** `keys` must be in base58 idpub format.                                                                                                                                                                                                                                                                                                                                                                                                                                                  | **at least 1 key is required.** </br> An empty array of strings was provided for `keys` parameter. </br></br> **"*invalid key*" key is invalid.** </br> An invalid key for `keys` parameter was provided. `keys` must be in base58 idpub format.</br></br> ***"duplicated key"* key is duplicated; keys must be unique.** </br> A duplicate key for the `keys` parameter was provided. </br></br> **keys must be an array.** </br> An invalid `keys` format was provided. </br></br> **calculated bytes of names and keys is <*totalBytes*>. It must be less than 10240, use less/shorter names or less keys.** </br> Too many `names` or `keys` were provided resulting in calculated bytes being larger than 10kb.
| `callback_url`    | optional | string </br> The URL you would like the callbacks to be sent to. </br> **Note:** If this is not specified, callbacks will not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **callback_url is an invalid url format.** </br> An invalid `callback_url` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `callback_stages` | optional | array of strings </br> The immutability stages you would like to be notified about. This list can include any or all of these three stages: `replicated`, `factom`, and `anchored`. For example: when you would like to trigger the callback from Connect at `replicated` and `factom` stage, you would send them in the format: [‘replicated’, ‘factom’]. </br> **Note:** For this field to matter, the URL must be provided. If callbacks are activated (URL has been specified) and this field is not sent, it will default to `factom` and `anchored`. | **callback_stages must be an array.** </br> An invalid `callback_stages` format was provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

**Returns**

**Response:** Accepted
-   **chain_id**: string </br> The unique identifier of the chain that has been created for this identity.
-   **entry_hash:** string </br> The unique identifier of the first entry that has been created in this identity chain.
-   **stage:** string </br> The current immutability stage of the identity chain and its first entry.
-   **key_pairs:** an array of objects </br> The 3 key pairs generated automatically by Factom SDK. This value is not returned if the public keys are provided when creating this identity.
    - **key_pairs[].private_key:** string </br> The private key in base58 Idsec format. 
    - **key_pairs[].public_key:** string </br> The public key in base58 Idpub format. </br>

```python
{
   'stage':'replicated',
   'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
   'chain_id':'107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42',
   'key_pairs':[
      {
         'private_key':'idsec1fKP8B6csh3yAHMiEu2x8NBBJvx7nkWhbJB6XvRobaKibvbMy2',
         'public_key':'idpub2EDrNudZUKBfKfppPXeeTZJVU4nzMCXQf9vicDeApafbzV3iXa'
      },
      {
         'private_key':'idsec2PY5YdmmMDDVrvkHctfFjbZybe3NSAPbtr9aJJTLrVj4tekXGx',
         'public_key':'idpub1mxNZop6vAGmutD87hdYz1hog1NnaSfFj3icTUiq6xUyjiiy89'
      },
      {
         'private_key':'idsec36HAy7vPMwCpDVeEDnGrkkW77W4QZ6rMvwrQ9tNP9JWgG6P2yv',
         'public_key':'idpub1zbpmSTnvErRkzoXus1hBmHSSFxvagqD3nZiMyna4JmnSnUDwF'
      }
   ]
}
```

### <a name="identities_get"></a>get

Gets a summary of the identity chain's current state.

**Sample**
```python
factom_client.identities.get('107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42')
```

**Parameters**

| **Name**                 | **Type** | **Description**                                                       | **SDK Error Message & Description**                                                   |
|--------------------------|----------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `identity_chain_id` | required | string </br> The unique identifier for the identity chain being requested. | **identity_chain_id is required.**  </br> `identity_chain_id` parameter was not provided. |

**Returns**

**Response:** OK
- **data:** object
- **data.version:** string </br> The identity chain's schema version. This details the format of this digital identity. For more information about the Factom identity schemas, view the documentation [here](https://docs.harmony.factom.com/docs/factom-signing-standard#section-factom-identity-chains).
- **data.stage:** string </br>  The immutability stage that this chain has reached. The identity can be considered active once it (and thus its keys) reaches the `factom` stage.
- **data.created_height:** integer </br> The block height at which this chain was written into the Factom blockchain. This is null if the chain has not reached the `factom` stage.
- **data.chain_id:** string</br> The unique identifier of this identity chain. 
- **data.names:** array of strings </br> A unique array of strings that together constitute the identity's name.</br>  **Note:** Since the Connect API Base64 encodes these values for transport, each array element will be decoded for you by the SDK.
- **data.all_keys_href:** string </br> An API link to retrieve the keys for this identity.
- **data.active_keys:** array of objects </br> An array of currently active public identity keys ordered from the highest to the lowest priority.
	-   **data.active_keys[].key:** string </br> The public key string in base58 idpub format.
	-   **data.active_keys[].activated_height:** integer </br> The height at which this key became active for this identity.
	-   **data.active_keys[].retired_height:** integer </br> The height at which this key was retired for this identity. This will be null if key is still active.
	-   **data.active_keys[].priority:** integer </br> The level of this key within the hierarchy. A lower number indicates a key that allows a holder to replace higher numbered keys. The master key is priority 0.
	-   **data.active_keys[].entry_hash:** string </br> The hash of the entry that was made documenting the key replacement.
- **data.pending_key:** object </br> A new public key that has been submitted as a replacement for a currently active key. Once the entry for the replacement is written into the blockchain, this key will become active and the replaced key will be retired.
	-  **data.pending_key.key:** string </br> The public key in base58 idpub format.
	-  **data.pending_key.activated_height:** integer </br> The height at which this key became active for this identity
	-  **data.pending_key.retired_height:** integer </br> The height at which this key was retired for this identity. This will be null if key is still active.
	-  **data.pending_key.priority:** integer </br> The level of this key within the hierarchy. A lower number indicates a key that allows a holder to replace higher numbered keys. The master key is priority 0.
	-  **data.pending_key.entry_hash:** string </br> The hash of the entry that was made documenting the key replacement. 



```python
{
   'data':{
      'stage':'replicated',
      'pending_key':None,
      'version':1,
      'active_keys':[
         {
            'activated_height':None,
            'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
            'key':'idpub2EDrNudZUKBfKfppPXeeTZJVU4nzMCXQf9vicDeApafbzV3iXa',
            'priority':0,
            'retired_height':None
         },
         {
            'activated_height':None,
            'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
            'key':'idpub1mxNZop6vAGmutD87hdYz1hog1NnaSfFj3icTUiq6xUyjiiy89',
            'priority':1,
            'retired_height':None
         },
         {
            'activated_height':None,
            'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
            'key':'idpub1zbpmSTnvErRkzoXus1hBmHSSFxvagqD3nZiMyna4JmnSnUDwF',
            'priority':2,
            'retired_height':None
         }
      ],
      'names':[
         'NotarySimulation',
         '2019-03-15T04:17:36.684136'
      ],
      'created_height':None,
      'all_keys_href':'/v1/identities/107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42/keys',
      'chain_id':'107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42'
   }
}
```
### <a name="identities_keys"></a>keys

##### <a name="keys_list"></a>list

Returns all of the keys that were ever active for this Identity. Results
are paginated. 

**Sample**
```python
factom_client.identities.keys.list('107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42')
```

**Parameters**

| **Name**                 | **Type** | **Description**                                                                                                                                                                                                                                                                                               | **SDK Error Message & Description** <img width=1400/>                                                                 |
|--------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `identity_chain_id` | required | string </br> The unique identifier of the identity chain whose keys are being requested.                                                                                                                                                                                                                 | **identity_chain_id is required.** </br> `identity_chain_id` parameter was not provided.          | |
| `limit`           | optional | integer </br> The maximum number of keys you would like to be returned. The default value is 15.                                                                                                                                                                                | **limit must be an integer.** </br> An invalid `limit` format was provided.                   |
| `offset`          | optional | integer </br> The key index (in number of keys from the first key) to start from in the list of all keys. For example, if you have already received the first 15 keys and you would like the next set, you would send an offset of 15. Default value is 0 which represents the first item. | **offset must be an integer.** </br> An invalid `offset` format was provided.                 |

**Returns**

**Response:** OK
-   **data:** array of objects </br> An array of public identity keys in the order that they were added to the identity.
	-   **data[].key:** string </br> The public key string in base58 idpub format.
	-   **data[].activated_height:** integer </br> The height at which this key became active for this identity.
	-   **data[].retired_height:** integer </br> The height at which this key was retired for this identity. The value will be null if the key is still active.
	-   **data[].priority:** integer </br>
The level of this key within the hierarchy. A lower number indicates a key that allows a holder </br> 
to replace higher numbered keys. The master key is priority 0. 
    - **data[].entry_hash:** string
 </br> The entry hash of the entry where this key was activated.

-   **offset**: integer </br> The index of the first key returned from the total set, which starts from 0.
-   **limit**: integer </br> The number of keys returned in the "data" object.
-   **count**: integer </br> The total number of keys found (both active and retired) for the identity.

```python
{
   'offset':0,
   'limit':15,
   'data':[
      {
         'activated_height':None,
         'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
         'key':'idpub1mxNZop6vAGmutD87hdYz1hog1NnaSfFj3icTUiq6xUyjiiy89',
         'priority':1,
         'retired_height':None
      },
      {
         'activated_height':None,
         'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
         'key':'idpub1zbpmSTnvErRkzoXus1hBmHSSFxvagqD3nZiMyna4JmnSnUDwF',
         'priority':2,
         'retired_height':None
      },
      {
         'activated_height':None,
         'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
         'key':'idpub2EDrNudZUKBfKfppPXeeTZJVU4nzMCXQf9vicDeApafbzV3iXa',
         'priority':0,
         'retired_height':None
      }
   ],
   'count':3
}
```
##### <a name="keys_get"></a>get

Gets information about a specific public key for a given Identity,
including the heights at which the key was activated and retired if
applicable.

**Sample**
```python
factom_client.identities.keys.get('107c8e488e95b63ca6fe1c409aa22c380b5c7be387d139c1cd0afaf608d1ae42', 
				  'idpub1zbpmSTnvErRkzoXus1hBmHSSFxvagqD3nZiMyna4JmnSnUDwF')
```

**Parameters**

| **Name**                 | **Type** | **Description**                                                                                   | **SDK Error Message & Description** <img width=400/>                                                                                                                              |
|--------------------------|----------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `identity_chain_id` | required | string </br> The unique identifier for the Identity that the key belongs to.                                | **identity_chain_id is required.** </br> `identity_chain_d` parameter was not provided.                                                                       |
| `key`             | required | string </br> The public key string to get information, which must be in base58 idpub format. | **key is required.** </br> `key` parameter was not provided. </br></br> **key is invalid.** </br> An invalid `key` format was provided. |

**Returns**

**Response:** OK
-   **data:** object
	-   **data.key:** string </br> The public key string in base58 idpub format.
	-   **data.activated_height:** integer </br> The height at which this key became active for this identity.
	-   **data.retired_height:** integer </br> The height at which this key was retired for this identity. The value can be null if key is still active.
	-   **data.priority:** integer </br> The level of this key within the hierarchy. The master key is priority 0. 
	-   **data.entry_hash:** string </br> The entry hash of the entry where this key was activated.

```python
{
   'data':{
      'activated_height':None,
      'entry_hash':'64e5c70cc7b58e3746e2e2e43c6a01b4b504512a3e87d39faf467823c43ccf1e',
      'key':'idpub1zbpmSTnvErRkzoXus1hBmHSSFxvagqD3nZiMyna4JmnSnUDwF',
      'priority':2,
      'retired_height':None
   }
}
```
##### <a name="keys_replace"></a>replace

Creates an entry in the Identity Chain for a key replacement, which means the old key will be deactivated (referred to as a “retired” key) and the new key will be activated. 

To do this, a user must send the key to be replaced (`old_public_key`), a signature authorizing the replacement and the public key that can be used to validate this signature. The signing key must be of an equal or higher level than the key that is being replaced.

This method will automatically generate a new key pair for you and return it. Optionally, you can provide your own new public key for a keypair you have generated yourself, at which time no keys will be returned. The key pair generated automatically by the SDK will be returned for you to save.

**Sample**
```python
 factom_client.identities.keys.replace('20ea6362994571c477e8b552fa38a6028760f2089ac1024fffee828279c9baa7',
				       'idpub1uAysiWct2XpmRSk7ydNHNRdtynXn46GwTKyPYM2t5q2chHaBA',
				       'idsec32pHEsJfcx98eBD4WTZDvAfxSwtFeyVy5ZSAad7R2dLgaurKkh')
```

**Parameters**

| **Name**                  | **Type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | **SDK Error Message & Description**    <img width=1800/>                                                                                                                                                                                                        |
|---------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `identity_chain_id`  | required | string </br> The unique identifier of the identity chain being requested                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **identity_chain_id is required.** </br> `identity_chain_id` parameter was not provided.                                                                                                                                                    |
| `old_public_key`     | required | base58 string in Idpub format </br>  The public key to be retired and replaced.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | **old_public_key is required.** </br> `old_public_key` parameter was not provided. </br></br>  **old_public_key is an invalid public key.** </br> An invalid `old_public_key` parameter was provided or key’s byte length is not equal to 41.   |
| `new_public_key`     | optional | base58 string in Idpub format </br> The new public key to be activated and take its place.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | **new_public_key is an invalid public key.** </br> An invalid `new_public_key` parameter was provided or key’s byte length is not equal to 41.                                                                                        |
| `signer_private_key` | required | base58 string in Idsec format </br> The private key to use to create the signature, which must be the same or higher priority than the public key to be replaced.                                                                                                                                                                                                                                                                                                                                                                                                                                                          | **signer_private_key is required.** </br> `signer_private_key` parameter was not provided. </br></br>  **signer_private_key is invalid.** </br> An invalid `signer_private_key` parameter was provided or key’s byte length is not equal to 41. |
| `callback_url`      | optional | string </br> The URL you would like the callbacks to be sent to. </br> **Note:** If this is not specified, callbacks will not be activated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | **callback_url is an invalid url format.** </br> An invalid `callback_url` format was provided.                                                                                                                                           |
| `callback_stages`   | optional | array of strings </br> The immutability stages you'd like to be notified about. This list can include any or all of these three stages: `replicated`, `factom`, and `anchored`. For example: when you would like to trigger the callback from Connect from `replicated` and `factom` then you should send them in the format: [‘replicated’, ‘factom’].  </br> **Note:** For this field to matter, the URL must be provided. If callbacks are activated (URL has been specified) and this field is not sent, it will default to `factom` and `anchored`. | **callback_stages must be an array.** </br> An invalid `callback_stages` format was provided.                                                                                                                                             |

**Returns**

**Response:** OK
-   **entry_hash:** string </br> The entry hash that will point to the key replacement entry on the blockchain.
-   **stage:** string </br> The current immutability stage of the new entry.
-   **key_pair:** object </br> The key pair generated automatically by the Factom SDK. This value will not be returned if the new public key is provided when calling this method. 
    - **key_pair.private_key:** string</br> 
    The private key in base58 Idsec format. 
    - **key_pair.public_key:** string</br> 
The public key in base58 Idpub format. 

    
```python
{
   'stage':'replicated',
   'entry_hash':'0fd4bdfead13b471cf47883223a843f454dae1d5bd29fff4cc308eda83d00c1d',
   'key_pair':{
      'private_key':'idsec2UQ8d9QK1gUZUJoDSmQtN4UJ1MvSvr64UDFGLuatCPvDaYx1Wj',
      'public_key':'idpub2Z7mJWCyUDensnQ5UcTxXUrQH9BsGDHjQbmNU5f3Rp3XpW7bYR'
   }
}
```
