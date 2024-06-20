const token = sessionStorage.getItem("userToken");

const backgroundMusic = document.getElementById("backgroundMusic");
const rollingSound = document.getElementById("rollingSound");
const winSound = document.getElementById("winSound");
const prizeSound = document.getElementById("prizeSound");
const noWinSound = document.getElementById("noWinSound");
const bonusRoundsSound = document.getElementById("bonusRoundsSound");
const endGameSound = document.getElementById("endGameSound");
const tumblingSound = document.getElementById("tumblingSound");
const explosionSound = document.getElementById("explosionSound");
const scatterSound = document.getElementById("scatterSound");

const muteButton = document.getElementById("muteButton");

let isMuted = false;
let isPlaying = false;

const borders = [
  "../images/challenger.webp",
  "../images/grand_master.webp",
  "../images/master.webp",
  "../images/platinum.webp",
  "../images/silver.webp",
  "../images/bronze.webp",
  "../images/bronze.webp",
  "../images/bronze.webp",
];

const symbols = [
  "../images/baiano.webp",
  "../images/mylon.webp",
  "../images/jime.webp",
  "../images/esa.webp",
  "../images/ranger.webp",
  "../images/brucer.webp",
  "../images/minerva.webp",
  "../images/bagre.jpeg",
];

const table = Array(7)
  .fill()
  .map(() => {
    return Array(7)
      .fill()
      .map(() => {
        const symbolIndex = Number.parseInt(Math.random() * (8 - 0) + 0);
        return {
          border: borders[symbolIndex],
          symbol: symbols[symbolIndex],
        };
      });
  }); // Initialize the table with default images

// Play background music
backgroundMusic.play();

function backToMenu() {
  window.location.href = "/menu?token=" + sessionStorage.getItem("userToken");
}

function toggleMute() {
  if (isMuted) {
    backgroundMusic.play();
    muteButton.textContent = "🔇";
  } else {
    backgroundMusic.pause();
    muteButton.textContent = "🔉";
  }
  isMuted = !isMuted;
}

function updateBetValue() {
  const betValue = document.getElementById("betValue").value;
  document.getElementById("betValueDisplay").textContent = betValue;
  document.getElementById("currentBet").textContent = `$ ${betValue}`;
  currentBet = betValue;
}

function updateAutoPlays() {
  const autoPlays = document.getElementById("autoPlays").value;
  document.getElementById("autoPlaysDisplay").textContent = autoPlays;
}

function renderTable() {
  const gameTable = document.getElementById("gameTable");
  gameTable.innerHTML = "";
  for (let row = 0; row < table.length; row++) {
    for (let col = 0; col < table.length; col++) {
      const cell = table[row][col];
      const cellDiv = document.createElement("div");
      cellDiv.className = "cell";
      cellDiv.dataset.row = row;
      cellDiv.dataset.col = col;

      const borderDiv = document.createElement("div");
      borderDiv.className = "border";
      borderDiv.style.backgroundImage = `url(${cell.border})`;

      const symbolContainer = document.createElement("div");
      symbolContainer.className = "symbol-container";
      symbolContainer.append(borderDiv);

      const symbolDiv = document.createElement("div");
      symbolDiv.className = "symbol";
      symbolDiv.style.backgroundImage = `url(${cell.symbol})`;
      symbolContainer.appendChild(symbolDiv);

      for (let i = 0; i < 10; i++) {
        // Add multiple symbols for better spinning effect
        const symbolIndex = Number.parseInt(Math.random() * (8 - 0) + 0);

        const borderDiv = document.createElement("div");
        borderDiv.className = "border";
        borderDiv.style.backgroundImage = `url(${borders[symbolIndex]})`;
        borderDiv.style.marginTop = `${150 * (i + 1)}px`;

        const symbolDiv = document.createElement("div");
        symbolDiv.className = "symbol";
        symbolDiv.style.backgroundImage = `url(${symbols[symbolIndex]})`;
        symbolDiv.style.marginTop = `${150 * (i + 1)}px`;
        symbolDiv.style.marginLeft = "-30px";

        symbolContainer.appendChild(borderDiv);
        symbolContainer.appendChild(symbolDiv);
      }

      cellDiv.appendChild(symbolContainer);
      gameTable.appendChild(cellDiv);
    }
  }
}

function startSpinning() {
  const cells = document.querySelectorAll(".symbol-container .symbol");
  cells.forEach((cell) => {
    cell.classList.add("spin-vertical");
  });

  const cells2 = document.querySelectorAll(".symbol-container .border");
  cells2.forEach((cell) => {
    cell.classList.add("spin-vertical");
  });
}

function stopSpinning() {
  const cells = document.querySelectorAll(".spin-vertical");
  cells.forEach((cell) => {
    cell.classList.remove("spin-vertical");
  });
}

function showAlert(message) {
  if (!message) return;

  const alert = document.getElementById("alert");
  alert.textContent = message;
  alert.classList.add("show");
  setTimeout(() => {
    alert.classList.remove("show");
  }, 3000);
}
let totalPlays = 0;
function play() {
  totalPlays = 0;
  const betValue = document.getElementById("betValue").value * 100;
  const autoPlays = document.getElementById("autoPlays").value;
  if (betValue == 0 || autoPlays == 0) {
    return showAlert("Please Set Bet Value and Auto Plays");
  }

  let timer = 500;
  for (let i = 0; i < autoPlays; i++) {
    fetch(`/playing?token=${token}&bet_value=${betValue}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((response) => {
        if (response.error) {
          showAlert(`Error: ${response.error}`);
        }

        for (let j = 0; j < response.length; j++) {
          const update = response[j];
          setTimeout(() => {
            UpdateHandler[update.action](update.data, j);
          }, timer); // 4 sec first roll action
          j == 0 ? (timer += 4000) : (timer += 2000); // 2 sec each other action
        }
      })
      .catch((error) => {
        showAlert(`Error: ${error}`);
      });
  }
}

const UpdateHandler = {
  fill_table: (data, action_number) => {
    if (action_number == 0) {
      totalPlays++;
      startSpinning();

      const betValueInput = document.getElementById("betValue");
      const autoPlaysInput = document.getElementById("autoPlays");
      const playButton = document.querySelector(".floating-play-button");
      const autoPlaysCount = document.getElementById("autoPlaysCount");

      betValueInput.setAttribute("disabled", "true");
      autoPlaysInput.setAttribute("disabled", "true");
      playButton.setAttribute("disabled", "true");

      walletBalanceDiv = document.querySelector("#walletBalance");
      let balance = Number.parseFloat(walletBalanceDiv.innerHTML.split(" ")[1]);
      balance -= betValueInput.value;
      walletBalanceDiv.innerHTML = `$ ${balance.toFixed(1)}`;

      autoPlaysCount.innerHTML = `${totalPlays}/${autoPlaysInput.value}`;
    }
    if (action_number == 0 && !isMuted) {
      rollingSound.play();
    } else if (!isMuted) {
      tumblingSound.play();
    }
    let timeout = 250;
    for (let i = 0; i < data.length; i++) {
      for (let j = 0; j < data.length; j++) {
        setTimeout(() => {
          const elements = document.querySelectorAll(
            `.cell[data-row="${j}"][data-col="${i}"] .spin-vertical`
          );
          elements.forEach((element) =>
            element.classList.remove("spin-vertical")
          );

          const border = document.querySelector(
            `.cell[data-row="${j}"][data-col="${i}"] .border`
          );
          const symbol = document.querySelector(
            `.cell[data-row="${j}"][data-col="${i}"] .symbol`
          );
          if (data[j][i].symbol == "../images/baiano.webp" && !isMuted) {
            scatterSound.play();
            border.classList.add("blinking");
            symbol.classList.add("blinking");
            setTimeout(() => {
              border.classList.remove("blinking");
              symbol.classList.remove("blinking");
            }, 1000);
          }
          const borderIndex = symbols.indexOf(data[j][i].symbol);
          border.style.backgroundImage = `url(${borders[borderIndex]})`;
          symbol.style.backgroundImage = `url(${data[j][i].symbol})`;
        }, timeout);
        timeout += 25;
      }
    }
  },
  find_clusters_and_update: (data, action_number) => {
    for (let i = 0; i < data.length; i++) {
      for (let j = 0; j < data.length; j++) {
        const cell = document.querySelector(
          `.cell[data-row="${i}"][data-col="${j}"] .symbol-container`
        );

        if (data[i][j].symbol == "🔥") {
          explosionSound.play();
          cell.classList.add("explosion");
          setTimeout(() => {
            const border = document.querySelector(
              `.cell[data-row="${i}"][data-col="${j}"] .border`
            );
            const symbol = document.querySelector(
              `.cell[data-row="${i}"][data-col="${j}"] .symbol`
            );
            cell.classList.remove("explosion");
            border.style.backgroundImage = "none";
            symbol.style.backgroundImage = "none";
          }, 1500);
        }
      }
    }
  },
  win_symbol: (data, action_number) => {
    if (!isMuted) winSound.play();

    winDiv = document.querySelector(".floating-win");
    winDiv.classList.add("blinking");
    winDiv.innerHTML = `<img src='${data.symbol.symbol}' width='40px' height='40px'> x ${data.size} pays $${data.amount}`;
    setTimeout(() => {
      winDiv.classList.remove("blinking");
    }, 1000);
  },
  tumble_table: (data, action_number) => {
    // UpdateHandler["fill_table"](data);
    for (let i = 0; i < data.length; i++) {
      for (let j = 0; j < data.length; j++) {
        const border = document.querySelector(
          `.cell[data-row="${i}"][data-col="${j}"] .border`
        );
        const symbol = document.querySelector(
          `.cell[data-row="${i}"][data-col="${j}"] .symbol`
        );

        if (data[i][j].symbol !== " ") {
          const borderIndex = symbols.indexOf(data[i][j].symbol);
          border.style.backgroundImage = `url(${borders[borderIndex]})`;
          symbol.style.backgroundImage = `url(${data[i][j].symbol})`;
        } else {
          border.style.backgroundImage = "none";
          symbol.style.backgroundImage = "none";
        }
      }
    }

    if (!isMuted) tumblingSound.play();
  },
  prize: (data, action_number) => {
    if (!isMuted) prizeSound.play();

    prizeDiv = document.querySelector(".floating-prize");
    prizeDiv.innerHTML = `Total win: $${data}`;
    prizeDiv.classList.add("blinking");
    setTimeout(() => {
      prizeDiv.classList.remove("blinking");
    }, 2000);
  },
  cash_in: (data, action_number) => {
    if (data > 0) {
      if (!isMuted) endGameSound.play();

      walletBalanceDiv = document.querySelector("#walletBalance");
      let balance = Number.parseFloat(walletBalanceDiv.innerHTML.split(" ")[1]);
      balance += data / 100;
      walletBalanceDiv.innerHTML = `$ ${balance.toFixed(1)}`;
    } else {
      if (!isMuted) noWinSound.play();
    }

    const bonusDiv = document.querySelector(".floating-bonus");
    bonusDiv.innerHTML = ` Get 3 or more
      <img src="../images/baiano.webp" width="40px" height="40px" />
      To win free spins`;

    const betValueInput = document.getElementById("betValue");
    const autoPlaysInput = document.getElementById("autoPlays");
    const playButton = document.querySelector(".floating-play-button");
    betValueInput.removeAttribute("disabled");
    autoPlaysInput.removeAttribute("disabled");
    playButton.removeAttribute("disabled");
  },
  bonus_rounds: (data, action_number) => {
    const bonusDiv = document.querySelector(".floating-bonus");
    bonusDiv.innerHTML = `Congrats you won ${data} Free Spins!`;

    if (!isMuted) {
      bonusRoundsSound.play();
    }

    const betValueInput = document.getElementById("betValue");
    const autoPlaysInput = document.getElementById("autoPlays");
    const playButton = document.querySelector(".floating-play-button");

    betValueInput.setAttribute("disabled", "true");
    autoPlaysInput.setAttribute("disabled", "true");
    playButton.setAttribute("disabled", "true");
  },
  round_n: (data, action_number) => {
    const bonusDiv = document.querySelector(".floating-bonus");
    bonusDiv.innerHTML = `Free spin ${data}`;

    if (!isMuted) {
      rollingSound.play();
    }
    startSpinning();
  },
};

// Initial render of the table
renderTable();
