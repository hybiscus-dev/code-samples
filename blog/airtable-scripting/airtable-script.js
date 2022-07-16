const TABLE_NAME = "<<REPLACE_WITH_TABLE_NAME>>";
const API_KEY = "<<REPLACE_WITH_API_KEY>>";

// Extract the table data from Airtable
let table = base.getTable(TABLE_NAME);
let query = await table.selectRecordsAsync({fields: table.fields});
let headings = table.fields.map(f => f.name);
let rows = [];
let row = [];
for (const record of query.records) {
    row = [];
    for (const field of table.fields) {
        let value = record.getCellValue(field.id);
        if (field.name === "Website") {
            row.push(`<a href="${value}">${value}</a>`);
        } else {
            row.push(value);
        }
    }
    rows.push(row);
}

// Creat the Table component for Hybiscus
const tableComponent = {
    "type": "Table",
    "options": {
        "headings": headings,
        "rows": rows
    }
}

// Assemble Hybiscus PDF report schema
const reportSchema = {
    "type": "Report",
    "options": {
        "report_title": "Market analysis",
        "report_byline": "Monthly market reports",
        "version_number": ""
    },
    "config": {
        "colour_theme": "candy",
        "typography_theme": "jost"
    },
    "components": [
        {
            "type": "Section",
            "options": {
                "section_title": "Competitors",
            },
            "components": [tableComponent]
        }
    ]
}

// Make API request
let response = await remoteFetchAsync('https://api.hybiscus.dev/api/v1/build-report', {
    method: 'POST',
    body: JSON.stringify(reportSchema),
    headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': API_KEY
    }
});
let jsonResponse = await response.json();
console.log(jsonResponse);
let taskID = jsonResponse.task_id;
let reportURL = `https://api.hybiscus.dev/api/v1/get-report?task_id=${taskID}&api_key=${API_KEY}`;
output.markdown(`[Report URL](${reportURL})`);