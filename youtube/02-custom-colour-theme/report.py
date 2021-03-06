import time
import json
import requests

PREFIX = "https://api.hybiscus.dev/api/v1"
REPORT_SCHEMA = {
    "type": "Report",
    "options": {
        "report_title": "Example.com",
        "report_byline": "Monthly analytics report",
        "version_number": "v0.1.0",
    },
    "config": {
        "typography_theme": "grotesque",
        "colour_theme": "default",
        "override_colour_theme": {
            "headline": "#042940",
            "sub-headline": "#000",
            "accent": "#005C53",
            "background": "#DEEFE7",
            "light-background": "white",
            "highlight": "#042940",
            "highlight-text": "#fff",
            "highlighted": {
                "sub-headline": "#042940",
                "background": "#fff",
                "light-background": "#DEEFE7",
                "highlight": "#005C53",
                "highlight-text": "#fff",
            },
        },
    },
    "components": [
        {
            "type": "Section",
            "options": {
                "section_title": "Overviews and KPI metrics",
                "highlighted": True,
                "columns": 3,
            },
            "components": [
                {
                    "type": "Card",
                    "options": {
                        "title": "Unique views",
                        "value": 987,
                        "units": "views",
                        "icon": "comet",
                    },
                },
                {
                    "type": "Card",
                    "options": {
                        "title": "Total sales",
                        "value": "53,476",
                        "units": "$",
                        "icon": "coin",
                        "highlighted": True,
                    },
                },
                {
                    "type": "Card",
                    "options": {
                        "title": "Product views",
                        "value": "1,362",
                        "units": "views",
                        "icon": "building-store",
                    },
                },
                {
                    "type": "Card",
                    "options": {
                        "title": "New customers",
                        "value": "321",
                        "icon": "users",
                    },
                },
                {
                    "type": "Card",
                    "options": {
                        "title": "Returning customers",
                        "value": "98",
                        "icon": "user-check",
                    },
                },
                {
                    "type": "Card",
                    "options": {
                        "title": "Bounce rate",
                        "value": "0.89",
                        "units": "%",
                        "icon": "arrow-back",
                    },
                },
            ],
        },
        {
            "type": "Section",
            "options": {"section_title": "Electronics product category"},
            "components": [
                {
                    "type": "Text",
                    "options": {
                        "width": "1/3",
                        "text": "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Repudiandae provident ipsa culpa officiis illum commodi voluptas, sequi repellat veniam adipisci laboriosam amet nesciunt nam explicabo.",
                    },
                },
                {
                    "type": "Row",
                    "options": {"columns": 2, "width": "2/3"},
                    "components": [
                        {
                            "type": "Card",
                            "options": {
                                "title": "Click through rate",
                                "value": "5",
                                "units": "%",
                                "icon": "click",
                            },
                        },
                        {
                            "type": "Card",
                            "options": {
                                "title": "Impressions",
                                "value": "1,364",
                                "units": "views",
                                "icon": "chart-area-line",
                                "highlighted": True,
                            },
                        },
                        {
                            "type": "Card",
                            "options": {
                                "title": "Total sales",
                                "value": "3,567",
                                "units": "$",
                                "icon": "coin",
                            },
                        },
                        {
                            "type": "Card",
                            "options": {
                                "title": "Product views",
                                "value": "1,018",
                                "units": "views",
                                "icon": "building-store",
                            },
                        },
                    ],
                },
            ],
        },
        {
            "type": "Section",
            "options": {"section_title": "Key performing pages"},
            "components": [
                {
                    "type": "Table",
                    "options": {
                        "title": "",
                        "headings": ["URL", "Page title", "Views"],
                        "striped": True,
                        "rows": [
                            [
                                "/products/arduino",
                                "Arduino accessories",
                                "9,342",
                            ],
                            [
                                "/products/raspberry-pi",
                                "Raspberry Pi accessories",
                                "5,674",
                            ],
                            ["/products/keyboards", "Keyboards", "2,248"],
                            [
                                "/products/graphics-cards",
                                "Graphics cards",
                                "973",
                            ],
                        ],
                    },
                }
            ],
        },
        {
            "type": "Section",
            "options": {
                "section_title": "Top performing referrers (highlighted)",
                "highlighted": True,
            },
            "components": [
                {
                    "type": "Table",
                    "options": {
                        "title": "",
                        "headings": ["Referrer", "URL", "Count"],
                        "striped": True,
                        "rows": [
                            [
                                "Google",
                                "google.com/search?s=raspberryi+pi",
                                "13,934",
                            ],
                            [
                                "Bing",
                                "bing.com/search?s=raspberry+pi",
                                "9,231",
                            ],
                            ["Facebook", "facebook.com", "3,673"],
                            ["Twitter", "twitter.com", "2,190"],
                        ],
                    },
                }
            ],
        },
    ],
}


response = requests.post(
    url=f"{PREFIX}/build-report",
    headers={
        "X-API-KEY": "<<API_KEY>>"
    },
    data=json.dumps(REPORT_SCHEMA),
)

task_id = response.json().get("task_id", None)
if task_id is None:
    print(response.content.decode())
    raise Exception("Something went wrong. Please check your schema.")

response = {}
while response.get("status", None) != "SUCCESS":
    response = requests.get(
        url=f"{PREFIX}/get-task-status",
        headers={
            "X-API-KEY": "<<API_KEY>>"
        },
        params={"task_id": task_id},
    )
    response = response.json()
    print(response)
    time.sleep(2)

print(
    f"Report URL: {PREFIX}/get-report?task_id={task_id}&api_key=<<API_KEY>>"
)
