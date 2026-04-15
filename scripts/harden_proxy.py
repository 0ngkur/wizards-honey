import os
import sys
import shutil
import base64

SHIELD_JS = """
import { machineIdSync } from "node-machine-id";
import crypto from "crypto";

export const WizardShield = {
    encrypt: (t) => {
        const k = crypto.createHash('sha256').update(machineIdSync() + "salt").digest();
        const iv = crypto.randomBytes(16);
        const c = crypto.createCipheriv('aes-256-cbc', k, iv);
        return iv.toString('hex') + ':' + Buffer.concat([c.update(t), c.final()]).toString('hex');
    },
    decrypt: (t) => {
        try {
            const k = crypto.createHash('sha256').update(machineIdSync() + "salt").digest();
            const [i, e] = t.split(':');
            const d = crypto.createDecipheriv('aes-256-cbc', k, Buffer.from(i, 'hex'));
            return Buffer.concat([d.update(Buffer.from(e, 'hex')), d.final()]).toString();
        } catch(e) { return "[LOCKED]"; }
    }
};
"""

def patch_file(path, search, replace):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if search in content:
        new_content = content.replace(search, replace)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[+] Patched: {path}")

def main():
    print("--- Wizard Shield: Pro Hacking Protection v3.0 ---")
    target = input("Enter target directory path: ").strip()
    
    if not os.path.exists(target):
        print("Error: Target not found.")
        return

    # Infrastructure setup
    lib_dir = os.path.join(target, "src", "lib")
    os.makedirs(lib_dir, exist_ok=True)
    
    with open(os.path.join(lib_dir, "wizardShield.js"), 'w') as f:
        f.write(SHIELD_JS)
    print("[+] Shield Engine Installed.")

    # Patch Database (Specific for 9router-like systems)
    db_path = os.path.join(target, "src", "lib", "localDb.js")
    patch_file(db_path, 
               'apiKey: data.apiKey', 
               'apiKey: WizardShield.encrypt(data.apiKey)')
    
    print("\n[✔] System Hardened. Run 'npm install node-machine-id' to finalize.")

if __name__ == "__main__":
    main()
