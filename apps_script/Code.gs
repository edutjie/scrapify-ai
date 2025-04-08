const BASE_URL = "https://scrapify-ai.onrender.com";

function onInstall(e) {
  onOpen(e);
}

function onOpen(e) {
  const ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem("Set API Key & Settings", "openSettingsDialog")
    .addToUi();
}

function openSettingsDialog() {
  const html = HtmlService.createHtmlOutputFromFile("Settings")
    .setWidth(400)
    .setHeight(300);
  SpreadsheetApp.getUi().showModalDialog(html, "LLM Settings");
}

function saveSettings(apiKey, temperature, model) {
  const userProps = PropertiesService.getUserProperties();
  userProps.setProperty("OPENAI_API_KEY", apiKey);
  userProps.setProperty("TEMPERATURE", temperature);
  userProps.setProperty("MODEL", model);
}

function getApiKey_() {
  const scriptProperties = PropertiesService.getUserProperties();
  const apiKey = scriptProperties.getProperty("OPENAI_API_KEY");
  if (!apiKey) {
    throw new Error(
      "API key not set. Go to Add-ons > Scrapify Settings to set it."
    );
  }
  return apiKey;
}

function postRequest_(endpoint, payload) {
  const apiKey = getApiKey_();
  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "x-api-key": apiKey,
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true,
  };

  const res = UrlFetchApp.fetch(BASE_URL + endpoint, options);
  const json = JSON.parse(res.getContentText());
  return json.response || "";
}

function CHAT(query) {
  return postRequest_("/api/chat", {
    query,
    model: "gpt-4o-mini",
    temperature: 0.5,
  });
}

function WEBSEARCH(query, searchInstructions) {
  return postRequest_("/api/websearch", {
    query,
    search_instructions: searchInstructions || "",
    model: "gpt-4o-mini",
  });
}

function SCRAPE_WEB(webUrl, query) {
  return postRequest_("/api/scrape", {
    web_url: webUrl,
    query,
    model: "gpt-4o-mini",
  });
}

function COMPANY_LINKEDIN(linkedinUrl) {
  const response = postRequest_("/api/company", {
    linkedin_url: linkedinUrl,
  });
  if (typeof response === "object") {
    return [
      [
        response.name,
        response.linkedin_internal_id,
        response.website,
        response.industry,
        response.company_size,
        response.company_size_on_linkedin,
        response.hq_location,
        response.company_type,
        response.founded_year,
        response.tagline,
      ],
    ];
  }
  return ["No response or invalid data"];
}

function PERSON_LOOKUP(companyUrl, role) {
  return postRequest_("/api/person-lookup", {
    company_url: companyUrl,
    role,
  });
}
