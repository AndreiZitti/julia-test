class GenderClassificationApp {
  constructor() {
    this.currentFile = null;
    this.currentColumns = [];
    this.selectedColumn = "";
    this.processedFilename = "";
    this.useAI = false;
    this.apiKey = "";

    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // File upload elements
    const uploadArea = document.getElementById("uploadArea");
    const fileInput = document.getElementById("fileInput");
    const uploadLink = document.querySelector(".upload-link");

    // Column selection elements
    const columnSelect = document.getElementById("columnSelect");
    const columnInput = document.getElementById("columnInput");

    // Classification method elements
    const useRuleBasedRadio = document.getElementById("useRuleBased");
    const useAIRadio = document.getElementById("useAI");
    const apiKeySection = document.getElementById("apiKeySection");
    const apiKeyInput = document.getElementById("apiKeyInput");
    const toggleApiKey = document.getElementById("toggleApiKey");

    // Action buttons
    const processBtn = document.getElementById("processBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const resetBtn = document.getElementById("resetBtn");

    // File upload events
    uploadArea.addEventListener("click", () => fileInput.click());
    uploadLink.addEventListener("click", (e) => {
      e.stopPropagation();
      fileInput.click();
    });

    fileInput.addEventListener("change", (e) =>
      this.handleFileSelect(e.target.files[0])
    );

    // Drag and drop events
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", () => {
      uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileSelect(files[0]);
      }
    });

    // Column selection events
    columnSelect.addEventListener("change", (e) => {
      if (e.target.value) {
        columnInput.value = "";
        this.selectedColumn = e.target.value;
        this.previewColumn();
      }
    });

    columnInput.addEventListener("input", (e) => {
      if (e.target.value.trim()) {
        columnSelect.value = "";
        this.selectedColumn = e.target.value.trim();
        this.previewColumn();
      }
    });

    // Classification method events
    useRuleBasedRadio.addEventListener("change", () =>
      this.handleMethodChange()
    );
    useAIRadio.addEventListener("change", () => this.handleMethodChange());
    apiKeyInput.addEventListener("input", (e) => {
      this.apiKey = e.target.value.trim();
      this.updateProcessButton();
    });

    // Toggle API key visibility
    toggleApiKey.addEventListener("click", () => {
      const apiKeyInput = document.getElementById("apiKeyInput");
      const toggleIcon = document.getElementById("toggleIcon");

      if (apiKeyInput.type === "text") {
        apiKeyInput.type = "password";
        toggleIcon.textContent = "🙈";
      } else {
        apiKeyInput.type = "text";
        toggleIcon.textContent = "👁️";
      }
    });

    // Action button events
    processBtn.addEventListener("click", () => this.processFile());
    downloadBtn.addEventListener("click", () => this.downloadFile());
    resetBtn.addEventListener("click", () => this.resetApp());
  }

  async handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      this.showMessage(
        "Please select a valid Excel file (.xlsx or .xls)",
        "error"
      );
      return;
    }

    // Validate file size (16MB limit)
    if (file.size > 16 * 1024 * 1024) {
      this.showMessage("File size must be less than 16MB", "error");
      return;
    }

    this.currentFile = file;
    this.showMessage(
      `File "${file.name}" selected successfully! Now select the column containing names.`,
      "success"
    );

    // Get column information without requiring a selected column first
    await this.getFileColumns();
  }

  async getFileColumns() {
    if (!this.currentFile) return;

    const formData = new FormData();
    formData.append("file", this.currentFile);

    try {
      const response = await fetch("/columns", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        this.currentColumns = result.columns;
        this.populateColumnSelect();
        this.showStep(2);
      } else {
        this.showMessage(result.error, "error");
      }
    } catch (error) {
      this.showMessage("Error reading file: " + error.message, "error");
    }
  }

  async uploadFile() {
    if (!this.currentFile || !this.selectedColumn) return;

    const formData = new FormData();
    formData.append("file", this.currentFile);
    formData.append("column_name", this.selectedColumn);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        this.currentColumns = result.columns;
        this.populateColumnSelect();
        this.showStep(2);
        this.showMessage(
          "File uploaded successfully! Please select the name column.",
          "success"
        );
      } else {
        this.showMessage(result.error, "error");
      }
    } catch (error) {
      this.showMessage("Error uploading file: " + error.message, "error");
    }
  }

  populateColumnSelect() {
    const columnSelect = document.getElementById("columnSelect");
    columnSelect.innerHTML = '<option value="">-- Select a column --</option>';

    this.currentColumns.forEach((column) => {
      const option = document.createElement("option");
      option.value = column;
      option.textContent = column;
      columnSelect.appendChild(option);
    });
  }

  async previewColumn() {
    if (!this.currentFile || !this.selectedColumn) return;

    const formData = new FormData();
    formData.append("file", this.currentFile);
    formData.append("column_name", this.selectedColumn);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        this.showColumnPreview(result);
        this.showStep(3);
      } else {
        this.showMessage(result.error, "error");
      }
    } catch (error) {
      this.showMessage("Error previewing column: " + error.message, "error");
    }
  }

  showColumnPreview(data) {
    const previewSection = document.getElementById("previewSection");
    const selectedColumnName = document.getElementById("selectedColumnName");
    const totalRows = document.getElementById("totalRows");
    const previewData = document.getElementById("previewData");

    selectedColumnName.textContent = data.selected_column;
    totalRows.textContent = data.total_rows;

    // Show preview data
    previewData.innerHTML = "";
    data.preview.forEach((item, index) => {
      const div = document.createElement("div");
      div.className = "preview-item";
      div.textContent = `${index + 1}. ${item || "[Empty]"}`;
      previewData.appendChild(div);
    });

    previewSection.style.display = "block";
  }

  handleMethodChange() {
    const useAI = document.getElementById("useAI").checked;
    const apiKeySection = document.getElementById("apiKeySection");

    this.useAI = useAI;

    if (useAI) {
      apiKeySection.style.display = "block";
    } else {
      apiKeySection.style.display = "none";
      this.apiKey = "";
      document.getElementById("apiKeyInput").value = "";
    }

    this.updateProcessButton();
  }

  updateProcessButton() {
    const processBtn = document.getElementById("processBtn");
    const processBtnText = document.getElementById("processBtnText");

    if (this.useAI) {
      if (this.apiKey) {
        processBtn.disabled = false;
        processBtnText.textContent = "🤖 Classify Names with AI";
      } else {
        processBtn.disabled = true;
        processBtnText.textContent = "🔑 Enter API Key to Continue";
      }
    } else {
      processBtn.disabled = false;
      processBtnText.textContent = "📚 Classify Names (Rule-Based)";
    }
  }

  async processFile() {
    if (!this.currentFile || !this.selectedColumn) {
      this.showMessage("Please select a file and column first", "error");
      return;
    }

    if (this.useAI && !this.apiKey) {
      this.showMessage(
        "Please enter your OpenAI API key to use AI classification",
        "error"
      );
      return;
    }

    const loading = document.getElementById("loading");
    const loadingText = document.getElementById("loadingText");
    const processBtn = document.getElementById("processBtn");

    // Show loading state
    processBtn.style.display = "none";
    loading.style.display = "block";

    if (this.useAI) {
      loadingText.textContent =
        "AI is analyzing names... This may take a moment";
    } else {
      loadingText.textContent = "Processing names... Please wait";
    }

    const formData = new FormData();
    formData.append("file", this.currentFile);
    formData.append("column_name", this.selectedColumn);
    formData.append("use_ai", this.useAI.toString());
    if (this.useAI) {
      formData.append("api_key", this.apiKey);
    }

    try {
      const response = await fetch("/process", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        this.processedFilename = result.filename;
        this.showResults(result);
        this.showStep(4);
        this.showMessage("File processed successfully!", "success");
      } else {
        // Show detailed error message for AI failures
        let errorMessage = result.error || "Processing failed";
        if (errorMessage.includes("AI Classification Failed")) {
          // Make AI errors more prominent
          this.showMessage(errorMessage, "error");

          // Show suggestions for common AI issues
          if (errorMessage.includes("Invalid API key")) {
            this.showMessage(
              "💡 Tip: Get a new API key at https://platform.openai.com/api-keys",
              "info"
            );
          } else if (errorMessage.includes("credits")) {
            this.showMessage(
              "💡 Tip: Add credits at https://platform.openai.com/account/billing",
              "info"
            );
          } else if (errorMessage.includes("models failed")) {
            this.showMessage(
              "💡 Tip: Try using the Rule-Based method instead, or contact OpenAI support",
              "info"
            );
          }
        } else {
          this.showMessage(errorMessage, "error");
        }
        processBtn.style.display = "block";
      }
    } catch (error) {
      this.showMessage("Error processing file: " + error.message, "error");
      processBtn.style.display = "block";
    } finally {
      loading.style.display = "none";
    }
  }

  showResults(data) {
    const classificationMethodUsed = document.getElementById(
      "classificationMethodUsed"
    );
    const resultsSummary = document.getElementById("resultsSummary");

    // Show classification method used
    classificationMethodUsed.innerHTML = `
      <strong>Classification Method:</strong> ${
        data.classification_method || "Rule-based"
      }
    `;

    const html = `
            <h3>🎯 Classification Results</h3>
            <div class="result-stat">
                <div class="number">${data.counts["1"] || 0}</div>
                <div class="label">👨 Males</div>
            </div>
            <div class="result-stat">
                <div class="number">${data.counts["2"] || 0}</div>
                <div class="label">👩 Females</div>
            </div>
            <div class="result-stat">
                <div class="number">${data.counts["?"] || 0}</div>
                <div class="label">❓ Uncertain</div>
            </div>
            <div class="result-stat">
                <div class="number">${data.total_processed}</div>
                <div class="label">📊 Total Processed</div>
            </div>
        `;

    resultsSummary.innerHTML = html;
  }

  async downloadFile() {
    if (!this.processedFilename) {
      this.showMessage("No processed file available", "error");
      return;
    }

    try {
      const response = await fetch(`/download/${this.processedFilename}`);

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = this.processedFilename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        this.showMessage("File downloaded successfully!", "success");
      } else {
        this.showMessage("Error downloading file", "error");
      }
    } catch (error) {
      this.showMessage("Error downloading file: " + error.message, "error");
    }
  }

  resetApp() {
    // Reset all state
    this.currentFile = null;
    this.currentColumns = [];
    this.selectedColumn = "";
    this.processedFilename = "";
    this.useAI = false;
    this.apiKey = "";

    // Reset form elements
    document.getElementById("fileInput").value = "";
    document.getElementById("columnSelect").innerHTML =
      '<option value="">-- Select a column --</option>';
    document.getElementById("columnInput").value = "";

    // Reset classification method
    document.getElementById("useRuleBased").checked = true;
    document.getElementById("useAI").checked = false;
    document.getElementById("apiKeyInput").value = "";
    document.getElementById("apiKeySection").style.display = "none";

    // Reset process button
    this.updateProcessButton();

    // Hide all steps except the first
    this.showStep(1);

    // Clear messages
    this.hideMessage();

    this.showMessage("Ready to process a new file!", "info");
  }

  showStep(stepNumber) {
    // Hide all steps
    for (let i = 1; i <= 4; i++) {
      const step = document.getElementById(`step${i}`);
      if (step) {
        step.style.display = i <= stepNumber ? "block" : "none";
      }
    }
  }

  showMessage(text, type = "info") {
    const messageEl = document.getElementById("message");
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;
    messageEl.style.display = "block";

    // Auto-hide success and info messages after 5 seconds
    if (type === "success" || type === "info") {
      setTimeout(() => this.hideMessage(), 5000);
    }
  }

  hideMessage() {
    const messageEl = document.getElementById("message");
    messageEl.style.display = "none";
  }
}

// Initialize the app when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new GenderClassificationApp();
});
