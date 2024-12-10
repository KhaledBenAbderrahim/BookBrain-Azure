import azure.functions as func
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    script_path = os.path.abspath(os.path.dirname(__file__))
    swagger_path = os.path.join(script_path, 'swagger.json')

    try:
        with open(swagger_path, 'r') as swagger_file:
            swagger_content = json.load(swagger_file)
        
        html_content = create_html_content(swagger_content)
        
        return func.HttpResponse(
            body=html_content,
            mimetype="text/html",
            status_code=200
        )
    except FileNotFoundError:
        return func.HttpResponse(
            "swagger.json file not found",
            status_code=404
        )
    except Exception as e:
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )

def create_html_content(swagger_spec):
    overview_html = """
    <div class="bg-gradient-to-r from-gray-800 to-blue-900 text-white p-6 md:p-12 mb-6 md:mb-10 rounded-lg shadow-2xl">
        <h1 class="text-3xl md:text-4xl font-bold mb-2 md:mb-4">Lernplattform: Kernfunktionen</h1>
        <p class="text-lg md:text-xl mb-4 md:mb-6">Eine Übersicht der zentralen Funktionen und Leistungsmerkmale der Lernplattform.</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-10 mb-8 md:mb-12">
        <div class="bg-white p-6 md:p-8 rounded-lg shadow-lg hover:shadow-2xl transition duration-300 border-t-4 border-blue-500">
            <div class="flex items-center mb-4 md:mb-6">
                <svg class="w-8 h-8 md:w-10 md:h-10 mr-3 md:mr-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                <h2 class="text-xl md:text-2xl font-semibold text-gray-800">Lernfortschrittsanalyse</h2>
            </div>
            <p class="text-sm md:text-base text-gray-600 mb-4 md:mb-6">Die Lernfortschrittsanalyse bietet eine umfassende Übersicht über die Lernaktivitäten der letzten zwei Wochen. Diese Funktion dient als objektiver Indikator für den individuellen Lernfortschritt.</p>
            <ul class="list-disc list-inside text-sm md:text-base text-gray-700 space-y-1 md:space-y-2">
                <li>Tägliche Lernzeiterfassung in Minuten</li>
                <li>Quantitative Erfassung absolvierter und bestandener Tests</li>
                <li>Fachspezifische Erfolgsquoten</li>
                <li>Detaillierte Fortschrittsanalyse verschiedener Lernbereiche</li>
            </ul>
        </div>
        
        <div class="bg-white p-6 md:p-8 rounded-lg shadow-lg hover:shadow-2xl transition duration-300 border-t-4 border-green-500">
            <div class="flex items-center mb-4 md:mb-6">
                <svg class="w-8 h-8 md:w-10 md:h-10 mr-3 md:mr-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                <h2 class="text-xl md:text-2xl font-semibold text-gray-800">PDF-Verarbeitungssystem</h2>
            </div>
            <p class="text-sm md:text-base text-gray-600 mb-4 md:mb-6">Das PDF-Verarbeitungssystem transformiert hochgeladene PDF-Dokumente in optimierte, lerngerechte Formate. Diese Funktion ermöglicht eine effiziente Integration neuer Lernmaterialien in die Plattform.</p>
            <ul class="list-disc list-inside text-sm md:text-base text-gray-700 space-y-1 md:space-y-2">
                <li>Fortschrittliche Texterkennung und -extraktion</li>
                <li>Automatisierte Segmentierung in didaktisch sinnvolle Einheiten</li>
                <li>Inhaltliche Analyse und thematische Kategorisierung</li>
                <li>Erstellung durchsuchbarer Textfragmente für schnellen Zugriff</li>
                <li>Datenbankintegration zur Optimierung von Abfragen</li>
            </ul>
        </div>
        
        <div class="bg-white p-6 md:p-8 rounded-lg shadow-lg hover:shadow-2xl transition duration-300 border-t-4 border-purple-500">
            <div class="flex items-center mb-4 md:mb-6">
                <svg class="w-8 h-8 md:w-10 md:h-10 mr-3 md:mr-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                <h2 class="text-xl md:text-2xl font-semibold text-gray-800">Buch-Upload-Funktionalität</h2>
            </div>
            <p class="text-sm md:text-base text-gray-600 mb-4 md:mb-6">Die Buch-Upload-Funktionalität ermöglicht eine reibungslose Integration neuer PDF-Bücher in die Lernplattform. Sie gewährleistet die Integrität und Verwendbarkeit der hochgeladenen Materialien.</p>
            <ul class="list-disc list-inside text-sm md:text-base text-gray-700 space-y-1 md:space-y-2">
                <li>Strikte Validierung des Dateiformats (PDF-Spezifikation)</li>
                <li>Automatisierte Extraktion und Verifizierung von Metadaten</li>
                <li>Sichere Speicherung unter Verwendung von Azure Blob Storage</li>
                <li>Automatische Initiierung des Verarbeitungsworkflows</li>
                <li>Implementierung von Duplikaterkennung zur Datenkonsistenz</li>
            </ul>
        </div>
    </div>
    
    <div class="bg-gray-100 p-6 md:p-8 rounded-lg shadow-lg mb-6 md:mb-10">
        <h3 class="text-xl md:text-2xl font-semibold mb-3 md:mb-4 text-gray-800">Anwendungsmöglichkeiten der API:</h3>
        <ol class="list-decimal list-inside text-sm md:text-base text-gray-700 space-y-2 md:space-y-3">
            <li>Nutzung des Lernfortschrittsanalyse-Endpunkts zur Generierung personalisierter Lernstatistiken und -empfehlungen.</li>
            <li>Einsatz der PDF-Verarbeitungsfunktion zur effizienten Integration und Aufbereitung neuer Lernmaterialien.</li>
            <li>Verwendung der Buch-Upload-Funktionalität zur Erweiterung der digitalen Bibliothek durch autorisierte Nutzer oder Administratoren.</li>
        </ol>
    </div>
    """

    return f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lernplattform API - Funktionsübersicht</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .hover-scale {{
            transition: transform 0.3s ease-in-out;
        }}
        .hover-scale:hover {{
            transform: scale(1.03);
        }}
        @media (max-width: 768px) {{
            .swagger-ui .wrapper {{
                padding: 0;
            }}
            .swagger-ui .opblock {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-6 md:py-12">
        {overview_html}
        <div id="swagger-ui" class="mt-6 md:mt-12"></div>
    </div>
    
    <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                spec: {json.dumps(swagger_spec)},
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
            }});

            // Benutzerdefiniertes Skript zur Verarbeitung der Metadaten
            ui.getSystem().on("beforeSend", function(request) {{
                if (request.url.endsWith("/UploadBookFunc")) {{
                    const formData = request.body;
                    const metadataFields = ['title', 'author', 'subtitle', 'isbn'];
                    const metadata = {{}};

                    metadataFields.forEach(field => {{
                        metadata[field] = formData.get(field);
                        formData.delete(field);
                    }});

                    formData.set('book_data', JSON.stringify(metadata));
                }}
            }});
        }}
    </script>
</body>
</html>
    """