// static/js/picture_board.js
// A small, self-contained picture/word board with optional delete buttons + speech.

(function () {
  class PictureBoard {
    /**
     * @param {string|HTMLElement} rootSelector
     * @param {Array<{id?:string, word:string, icon:string}>} items
     * @param {object} opts
     *  - lang: string (e.g. "en-GB")
     *  - editable: boolean (show X buttons)
     *  - onItemsChange: function(newItems)
     */
    constructor(rootSelector, items, opts = {}) {
      this.root = typeof rootSelector === "string" ? document.querySelector(rootSelector) : rootSelector;
      if (!this.root) throw new Error("PictureBoard root element not found");

      this.opts = {
        lang: opts.lang || "en-GB",
        editable: Boolean(opts.editable),
        onItemsChange: typeof opts.onItemsChange === "function" ? opts.onItemsChange : null,
      };

      this.items = Array.isArray(items) ? items.slice() : [];
      this.render();
    }

    setItems(items) {
      this.items = Array.isArray(items) ? items.slice() : [];
      this.render();
    }

    getItems() {
      return this.items.slice();
    }

    speak(text) {
      const t = (text || "").trim();
      if (!t) return;
      if (!("speechSynthesis" in window) || typeof SpeechSynthesisUtterance === "undefined") return;

      // Cancel any ongoing speech to keep it snappy for a child-facing UI.
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(t);
      utterance.lang = this.opts.lang;
      window.speechSynthesis.speak(utterance);
    }

    _emitChange() {
      if (this.opts.onItemsChange) {
        // Pass a deep-ish copy to avoid accidental shared mutation.
        this.opts.onItemsChange(this.items.map(i => ({ ...i })));
      }
    }

    removeById(id) {
      const before = this.items.length;
      this.items = this.items.filter(i => i.id !== id);
      if (this.items.length !== before) {
        this._emitChange();
        this.render();
      }
    }

    render() {
      // Clear
      this.root.innerHTML = "";

      const grid = document.createElement("div");
      grid.className = "pb-grid";

      for (const item of this.items) {
        const tile = document.createElement("div");
        tile.className = "pb-tile";
        tile.dataset.id = item.id || "";

        // IMPORTANT: speak button is inside a DIV tile (no nested buttons).
        const speakBtn = document.createElement("button");
        speakBtn.type = "button";
        speakBtn.className = "pb-speak";
        speakBtn.addEventListener("click", () => this.speak(item.word));

        const icon = document.createElement("div");
        icon.className = "pb-icon";
        icon.textContent = item.icon;

        const label = document.createElement("div");
        label.className = "pb-label";
        label.textContent = item.word;

        speakBtn.appendChild(icon);
        speakBtn.appendChild(label);

        tile.appendChild(speakBtn);

        if (this.opts.editable) {
          const del = document.createElement("button");
          del.type = "button";
          del.className = "pb-remove";
          del.setAttribute("aria-label", `Remove ${item.word}`);
          del.textContent = "×";

          del.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation(); // do not speak
            this.removeById(item.id);
          });

          tile.appendChild(del);
        }

        grid.appendChild(tile);
      }

      this.root.appendChild(grid);
    }
  }

  window.PictureBoard = PictureBoard;
})();
