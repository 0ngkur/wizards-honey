import { machineIdSync } from "node-machine-id";
import crypto from "crypto";

/**
 * Wizard Shield Core
 * Provides hardware-locked encryption and remote access protection.
 */

const ALGORITHM = 'aes-256-cbc';
const IV_LENGTH = 16;

// Generate a unique key based on the local machine hardware ID
const getShieldKey = () => {
    try {
        const id = machineIdSync();
        return crypto.createHash('sha256').update(id + "wizard-shield-salt-2026").digest();
    } catch (e) {
        return crypto.createHash('sha256').update("static-fallback-shield-key").digest();
    }
};

export const WizardShield = {
    encrypt: (text) => {
        if (!text) return text;
        const key = getShieldKey();
        const iv = crypto.randomBytes(IV_LENGTH);
        const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
        let encrypted = cipher.update(text);
        encrypted = Buffer.concat([encrypted, cipher.final()]);
        return iv.toString('hex') + ':' + encrypted.toString('hex');
    },
    decrypt: (text) => {
        if (!text || !text.includes(':')) return text;
        try {
            const key = getShieldKey();
            const [ivHex, encryptedHex] = text.split(':');
            const iv = Buffer.from(ivHex, 'hex');
            const encryptedText = Buffer.from(encryptedHex, 'hex');
            const decipher = crypto.createDecipheriv(ALGORITHM, key, iv);
            let decrypted = decipher.update(encryptedText);
            decrypted = Buffer.concat([decrypted, decipher.final()]);
            return decrypted.toString();
        } catch (e) {
            return "[ENCRYPTED_SHIELD_DATA]";
        }
    },
    isStrictLocal: (request) => {
        const remoteAddr = request.headers.get("x-forwarded-for") || 
                           request.headers.get("x-real-ip") || 
                           "remote";
        if (remoteAddr !== "remote" && remoteAddr !== "127.0.0.1" && remoteAddr !== "::1") {
            return false;
        }
        const host = (request.headers.get("host") || "").split(":")[0].toLowerCase();
        return host === "localhost" || host === "127.0.0.1" || host === "::1";
    },
    getHoneyKeys: () => {
        return [
            { id: "h-001", provider: "openai", name: "Production Key", apiKey: "sk-proj-wizard-" + crypto.randomBytes(12).toString('hex'), isActive: true },
            { id: "h-002", provider: "anthropic", name: "Staging Access", apiKey: "sk-ant-wizard-" + crypto.randomBytes(12).toString('hex'), isActive: true }
        ];
    }
};
