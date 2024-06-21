// Constants
const SOUND_FILES = {
  background: "backgroundMusic",
  rolling: "rollingSound",
  win: "winSound",
  prize: "prizeSound",
  noWin: "noWinSound",
  bonusRounds: "bonusRoundsSound",
  endGame: "endGameSound",
  tumbling: "tumblingSound",
  explosion: "explosionSound",
  scatter: "scatterSound",
  reRoll: "reRollSound",
};

const IMAGES = {
  borders: [
    "../images/challenger.webp",
    "../images/grand_master.webp",
    "../images/master.webp",
    "../images/platinum.webp",
    "../images/silver.webp",
    "../images/bronze.webp",
    "../images/bronze.webp",
    "../images/bronze.webp",
  ],
  symbols: [
    "../images/baiano.webp",
    "../images/mylon.webp",
    "../images/jime.webp",
    "../images/esa.webp",
    "../images/ranger.webp",
    "../images/brucer.webp",
    "../images/minerva.webp",
    "../images/bagre.jpeg",
  ],
};

const SELECTORS = {
  menuButton: "menuButton",
  muteButton: "muteButton",
  betValue: "betValue",
  betValueDisplay: "betValueDisplay",
  currentBet: "currentBet",
  autoPlays: "autoPlays",
  autoPlaysDisplay: "autoPlaysDisplay",
  gameTable: "gameTable",
  alert: "alert",
  walletBalance: "#walletBalance",
  floatingPlayButton: ".floating-play-button",
  autoPlaysCount: "autoPlaysCount",
  floatingWin: ".floating-win",
  floatingPrize: ".floating-prize",
  floatingBonus: ".floating-bonus",
};

// Helper Functions
function getElement(selector) {
  return document.getElementById(selector) || document.querySelector(selector);
}

function getElements(selector) {
  return document.querySelectorAll(selector);
}

function createElement(tag, className, attributes = {}, styles = {}) {
  const element = document.createElement(tag);
  element.className = className;

  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, value);
  });

  Object.entries(styles).forEach(([key, value]) => {
    element.style[key] = value;
  });

  return element;
}

// Audio Management
class AudioManager {
  constructor() {
    this.isMuted = false;
    this.sounds = this.initializeSounds();
  }

  initializeSounds() {
    const sounds = {};
    Object.entries(SOUND_FILES).forEach(([key, id]) => {
      sounds[key] = getElement(id);
    });
    return sounds;
  }

  toggleMute() {
    this.isMuted = !this.isMuted;
    if (this.isMuted) {
      this.sounds.background.pause();
      getElement(SELECTORS.muteButton).textContent = "🔉";
    } else {
      this.sounds.background.play();
      getElement(SELECTORS.muteButton).textContent = "🔇";
    }
  }

  playSound(name) {
    if (!this.isMuted && this.sounds[name]) {
      this.sounds[name].play();
    }
  }
}

// DOM Manipulation
class DOMManager {
  constructor(gameManager) {
    this.audioManager = new AudioManager();
    this.gameManager = gameManager;
    this.initializeEventListeners();
    this.audioManager.playSound("background");
  }

  initializeEventListeners() {
    getElement(SELECTORS.muteButton).addEventListener("click", () =>
      this.audioManager.toggleMute()
    );
    getElement(SELECTORS.floatingPlayButton).addEventListener("click", () =>
      this.gameManager.play()
    );
    getElement(SELECTORS.menuButton).addEventListener("click", () => {
      window.location.href = "/menu?token=" + this.gameManager.token;
    });

    this.updateElementAttribute(SELECTORS.betValue, "onchange", () => {
      this.updateTextContent(
        SELECTORS.betValueDisplay,
        getElement(SELECTORS.betValue).value
      );

      this.updateTextContent(
        SELECTORS.currentBet,
        `$ ${getElement(SELECTORS.betValue).value}`
      );
    });

    this.updateElementAttribute(SELECTORS.autoPlays, "onchange", () => {
      this.updateTextContent(
        SELECTORS.autoPlaysDisplay,
        getElement(SELECTORS.autoPlays).value
      );
    });
  }

  updateTextContent(selector, content) {
    const element = getElement(selector);
    if (element) {
      element.textContent = content;
    }
  }

  updateElementAttribute(selector, attribute, value) {
    const element = getElement(selector);
    if (element) {
      element[attribute] = value;
    }
  }

  showAlert(message) {
    if (!message) return;
    const alert = getElement(SELECTORS.alert);
    alert.textContent = message;
    alert.classList.add("show");
    setTimeout(() => alert.classList.remove("show"), 3000);
  }

  renderTable(table) {
    const gameTable = getElement(SELECTORS.gameTable);
    gameTable.innerHTML = "";

    table.forEach((row, rowIndex) => {
      row.forEach((cell, colIndex) => {
        const cellDiv = createElement("div", "cell", {
          "data-row": rowIndex,
          "data-col": colIndex,
        });

        const symbolContainer = createElement("div", "symbol-container");
        const borderDiv = createElement(
          "div",
          "border",
          {},
          {
            backgroundImage: `url(${cell.border})`,
          }
        );

        const symbolDiv = createElement(
          "div",
          "symbol",
          {},
          { backgroundImage: `url(${cell.symbol})` }
        );

        symbolContainer.append(borderDiv, symbolDiv);

        for (let i = 0; i < 10; i++) {
          const symbolIndex = Math.floor(Math.random() * IMAGES.symbols.length);
          const extraBorderDiv = createElement(
            "div",
            "border",
            {},
            {
              backgroundImage: `url(${IMAGES.borders[symbolIndex]})`,
              marginTop: `${150 * (i + 1)}px`,
            }
          );
          const extraSymbolDiv = createElement(
            "div",
            "symbol",
            {},
            {
              backgroundImage: `url(${IMAGES.symbols[symbolIndex]})`,
              marginTop: `${150 * (i + 1)}px`,
              marginLeft: "-30px",
            }
          );
          symbolContainer.append(extraBorderDiv, extraSymbolDiv);
        }

        cellDiv.append(symbolContainer);
        gameTable.append(cellDiv);
      });
    });
  }

  startSpinning() {
    this.toggleSpinning(true);
  }

  stopSpinning() {
    this.toggleSpinning(false);
  }

  toggleSpinning(isSpinning) {
    const elements = getElements(
      ".symbol-container .symbol, .symbol-container .border"
    );
    elements.forEach((element) => {
      element.classList.toggle("spin-vertical", isSpinning);
    });
  }
}

// Game Logic
class GameManager {
  constructor() {
    this.token = sessionStorage.getItem("userToken");
    this.domManager = new DOMManager(this);
    this.updateHandler = new UpdateHandler(this.domManager, this.token);
    this.autoPlays = 0;
    this.totalPlays = 0;
    this.initializeTable();
  }

  initializeTable() {
    this.table = Array.from({ length: 7 }, () =>
      Array.from({ length: 7 }, () => {
        const symbolIndex = Math.floor(Math.random() * IMAGES.symbols.length);
        return {
          border: IMAGES.borders[symbolIndex],
          symbol: IMAGES.symbols[symbolIndex],
        };
      })
    );
    this.domManager.renderTable(this.table);
  }

  play() {
    const betValue = parseInt(getElement(SELECTORS.betValue).value, 10) * 100;
    this.autoPlays = parseInt(getElement(SELECTORS.autoPlays).value, 10);
    if (betValue === 0 || this.autoPlays === 0) {
      return this.domManager.showAlert("Please Set Bet Value and Auto Plays");
    }

    let timer = 500;
    for (let i = 0; i < this.autoPlays; i++) {
      fetch(`/playing?token=${this.token}&bet_value=${betValue}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((response) => {
          if (response.error) {
            this.domManager.showAlert(`Error: ${response.error}`);
          }

          response.forEach((update, index) => {
            setTimeout(() => {
              this.handleUpdate(update, index);
            }, timer);
            timer += index === 0 ? 4000 : 2000;
          });
        })
        .catch((error) => {
          this.domManager.showAlert(`Error: ${error}`);
        });
    }
  }

  handleUpdate(update, actionNumber) {
    if (this.updateHandler[update.action]) {
      this.updateHandler[update.action](update.data, actionNumber);
    }
  }
}

// Update Handlers
class UpdateHandler {
  constructor(domManager, token) {
    this.domManager = domManager;
    this.token = token;
    this.totalPlays = 0;
  }

  fill_table(data, actionNumber) {
    if (actionNumber === 0) {
      this.totalPlays = 0;
      this.domManager.startSpinning();
      this.updateControls(true);
      this.updateWalletBalance();
      this.updateAutoPlaysCount();
      this.domManager.audioManager.playSound("rolling");
    } else {
      this.domManager.audioManager.playSound("reRoll");
    }

    for (let colIndex = 0; colIndex < data.length; colIndex++) {
      for (let rowIndex = 0; rowIndex < data.length; rowIndex++) {
        const cell = data[rowIndex][colIndex];

        setTimeout(() => {
          const spinningElements = getElements(
            `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .spin-vertical`
          );
          spinningElements.forEach((element) =>
            element.classList.remove("spin-vertical")
          );

          const border = getElement(
            `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .border`
          );
          const symbol = getElement(
            `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .symbol`
          );

          if (cell.symbol === IMAGES.symbols[0]) {
            this.domManager.audioManager.playSound("scatter");
            border.classList.add("blinking");
            symbol.classList.add("blinking");
            setTimeout(() => {
              border.classList.remove("blinking");
              symbol.classList.remove("blinking");
            }, 1000);
          }

          const borderIndex = IMAGES.symbols.indexOf(cell.symbol);
          border.style.backgroundImage = `url(${IMAGES.borders[borderIndex]})`;
          symbol.style.backgroundImage = `url(${cell.symbol})`;
        }, 250 * colIndex + 25 * rowIndex);
      }
    }
  }

  find_clusters_and_update(data) {
    data.forEach((row, rowIndex) => {
      row.forEach((cell, colIndex) => {
        const cellDiv = getElement(
          `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .symbol-container`
        );

        if (cell.symbol === "🔥") {
          this.domManager.audioManager.playSound("explosion");
          cellDiv.classList.add("explosion");
          setTimeout(() => {
            const border = getElement(
              `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .border`
            );
            const symbol = getElement(
              `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .symbol`
            );
            cellDiv.classList.remove("explosion");
            border.style.backgroundImage = "none";
            symbol.style.backgroundImage = "none";

            for (let k = rowIndex - 1; k >= 0; k--) {
              if (data[k][colIndex].symbol !== "🔥") {
                const container = getElement(
                  `.cell[data-row="${k}"][data-col="${colIndex}"]`
                );
                container.classList.add("fall-down");
              }
            }
          }, 1500);
        }
      });
    });
  }

  win_symbol(data) {
    this.domManager.audioManager.playSound("win");
    const winDiv = getElement(SELECTORS.floatingWin);
    winDiv.classList.add("blinking");
    winDiv.innerHTML = `<img src='${data.symbol.symbol}' width='40px' height='40px'> x ${data.size} pays $${data.amount}`;
    setTimeout(() => winDiv.classList.remove("blinking"), 1000);
  }

  tumble_table(data) {
    data.forEach((row, rowIndex) => {
      row.forEach((cell, colIndex) => {
        const border = getElement(
          `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .border`
        );
        const symbol = getElement(
          `.cell[data-row="${rowIndex}"][data-col="${colIndex}"] .symbol`
        );

        if (cell.symbol !== " ") {
          const borderIndex = IMAGES.symbols.indexOf(cell.symbol);
          border.style.backgroundImage = `url(${IMAGES.borders[borderIndex]})`;
          symbol.style.backgroundImage = `url(${cell.symbol})`;
        } else {
          border.style.backgroundImage = "none";
          symbol.style.backgroundImage = "none";
        }
      });
    });
    this.domManager.audioManager.playSound("tumbling");
    const fallingElements = getElements(".fall-down");
    fallingElements.forEach((element) => {
      element.classList.remove("fall-down");
    });
  }

  prize(data) {
    this.domManager.audioManager.playSound("prize");
    const prizeDiv = getElement(SELECTORS.floatingPrize);
    prizeDiv.innerHTML = `Total win: $${data}`;
    prizeDiv.classList.add("blinking");
    setTimeout(() => prizeDiv.classList.remove("blinking"), 2000);
  }

  cash_in(data) {
    if (data > 0) {
      this.domManager.audioManager.playSound("endGame");
      const walletBalanceDiv = getElement(SELECTORS.walletBalance);
      const balance = parseFloat(walletBalanceDiv.innerHTML.split(" ")[1]);
      walletBalanceDiv.innerHTML = `$ ${(balance + data / 100).toFixed(1)}`;
    } else {
      this.domManager.audioManager.playSound("noWin");
    }
    this.updateControls(false);
  }

  bonus_rounds(data) {
    this.domManager.updateTextContent(
      SELECTORS.floatingBonus,
      `Congrats you won ${data} Free Spins!`
    );
    this.domManager.audioManager.playSound("bonusRounds");
    this.updateControls(true);
  }

  round_n(data) {
    this.domManager.updateTextContent(
      SELECTORS.floatingBonus,
      `Free spin ${data}`
    );
    this.domManager.audioManager.playSound("rolling");
    this.domManager.startSpinning();
  }

  updateControls(isDisabled) {
    getElement(SELECTORS.betValue).disabled = isDisabled;
    getElement(SELECTORS.autoPlays).disabled = isDisabled;
    getElement(SELECTORS.floatingPlayButton).disabled = isDisabled;
  }

  updateWalletBalance() {
    const walletBalanceDiv = getElement(SELECTORS.walletBalance);
    let balance = parseFloat(walletBalanceDiv.innerHTML.split(" ")[1]);
    balance -= parseFloat(getElement(SELECTORS.betValue).value);

    this.domManager.updateTextContent(
      SELECTORS.walletBalance,
      `$ ${balance.toFixed(2)}`
    );
  }

  updateAutoPlaysCount() {
    this.totalPlays++;
    this.domManager.updateTextContent(
      SELECTORS.autoPlaysCount,
      `${this.totalPlays}/${getElement(SELECTORS.autoPlays).value}`
    );
  }
}

// Initialize Game
const gameManager = new GameManager();
