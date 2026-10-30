import json

# Ganti path ini jika Anda mengupload openapi.json ke Google Drive
FILE_PATH = 'openapi.json'

def generate_markdown_docs():
    try:
        with open(FILE_PATH, 'r') as f:
            spec = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{FILE_PATH}' tidak ditemukan. Pastikan Anda sudah mengunggahnya ke Colab.")
        return

    md_content = "# API Reference (Auto-Generated)\n\n"
    md_content += "Dokumen ini dibuat secara otomatis dari `openapi.json` FastAPI.\n\n"

    paths = spec.get('paths', {})
    
    for path, methods in paths.items():
        for method, details in methods.items():
            method_upper = method.upper()
            summary = details.get('summary', 'No summary')
            description = details.get('description', '')
            
            md_content += f"## `{method_upper} {path}`\n"
            md_content += f"**{summary}**\n\n"
            if description:
                md_content += f"{description}\n\n"
            
            # Body parameters
            request_body = details.get('requestBody', {})
            if request_body:
                content = request_body.get('content', {}).get('application/json', {})
                schema_ref = content.get('schema', {}).get('$ref', '')
                if schema_ref:
                    schema_name = schema_ref.split('/')[-1]
                    schema = spec.get('components', {}).get('schemas', {}).get(schema_name, {})
                    md_content += "**Request Body:**\n"
                    md_content += "| Field | Type | Required |\n|---|---|---|\n"
                    for prop, prop_details in schema.get('properties', {}).items():
                        ptype = prop_details.get('type', 'any')
                        md_content += f"| `{prop}` | `{ptype}` | Yes |\n"
                    md_content += "\n"
            
            md_content += "---\n\n"

    with open('API_REFERENCE.md', 'w') as f:
        f.write(md_content)
    
    print("✅ Dokumentasi API berhasil dibuat: 'API_REFERENCE.md'")
    print("Silakan download file tersebut dan taruh di folder /docs di repo GitHub Anda.")

if __name__ == "__main__":
    generate_markdown_docs()
