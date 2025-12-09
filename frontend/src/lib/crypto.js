import _sodium from 'libsodium-wrappers';

// Initialize sodium
let sodium;
const initSodium = async () => {
    await _sodium.ready;
    sodium = _sodium;
};

export const cryptoLib = {
    init: initSodium,

    // ChaCha20-Poly1305 for Text
    encryptChaCha: async (message, keyStr) => {
        if (!sodium) await initSodium();
        // Simple key derivation or usage (in prod use proper KDF)
        // Ensure key is 32 bytes
        const key = sodium.from_string(keyStr.padEnd(32, '0').slice(0, 32));
        const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
        const ciphertext = sodium.crypto_secretbox_easy(message, nonce, key);

        return {
            cipher: sodium.to_base64(ciphertext),
            nonce: sodium.to_base64(nonce)
        };
    },

    decryptChaCha: async (cipherObj, keyStr) => {
        if (!sodium) await initSodium();
        const key = sodium.from_string(keyStr.padEnd(32, '0').slice(0, 32));
        const nonce = sodium.from_base64(cipherObj.nonce);
        const ciphertext = sodium.from_base64(cipherObj.cipher);

        const decrypted = sodium.crypto_secretbox_open_easy(ciphertext, nonce, key);
        return sodium.to_string(decrypted);
    },

    // ChaCha20-Poly1305 for Binary (Benchmarking/Chaining)
    encryptChaChaBuffer: async (messageBytes, keyStr) => {
        if (!sodium) await initSodium();
        const key = sodium.from_string(keyStr.padEnd(32, '0').slice(0, 32));
        const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
        const ciphertext = sodium.crypto_secretbox_easy(messageBytes, nonce, key);
        return { cipher: ciphertext, nonce: nonce };
    },

    decryptChaChaBuffer: async (cipherObj, keyStr) => {
        if (!sodium) await initSodium();
        const key = sodium.from_string(keyStr.padEnd(32, '0').slice(0, 32));
        const decrypted = sodium.crypto_secretbox_open_easy(cipherObj.cipher, cipherObj.nonce, key);
        return decrypted;
    },

    // AES-256 for Files (using Web Crypto API for performance on large files)
    encryptAES: async (fileBlob) => {
        // Generate AES Key
        const key = await window.crypto.subtle.generateKey(
            { name: "AES-GCM", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );

        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const encrypted = await window.crypto.subtle.encrypt(
            { name: "AES-GCM", iv: iv },
            key,
            fileBlob
        );

        // Export key to send it (encrypted with ChaCha session key in real app)
        const exportedKey = await window.crypto.subtle.exportKey("raw", key);

        return {
            encrypted: new Uint8Array(encrypted),
            iv: iv,
            key: new Uint8Array(exportedKey)
        };
    },

    // Decrypt AES (helper)
    decryptAES: async (encryptedData, keyRaw, iv) => {
        const key = await window.crypto.subtle.importKey(
            "raw",
            keyRaw,
            { name: "AES-GCM" },
            true,
            ["decrypt"]
        );

        const decrypted = await window.crypto.subtle.decrypt(
            { name: "AES-GCM", iv: iv },
            key,
            encryptedData
        );
        return decrypted;
    }
};
