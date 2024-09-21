// Global variables
let currentPlayer = 0;
let players = [];

// Function to reset the game manager
async function resetGameManager() {
    await fetch('/forfeit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: ''
    });
    currentPlayer = 0;
    players = [];
    console.debug('Game Manager reset.');
}

// Fetch player names and initialize the turn indicator (only fetch once)
function fetchPlayers() {
    fetch('/get-players')
        .then(response => response.json())
        .then(data => {
            players = [...new Set(data.players)];  // Remove duplicates
            console.debug('Players:', players);
            updatePlayerTurn();  // Update the player turn UI
        })
        .catch(error => console.error('Error fetching players:', error));
}

// Initialize the game manager on page load
document.addEventListener('DOMContentLoaded', function() {
    //resetGameManager();
    fetchPlayers();
});

// Fetch player names and initialize the turn indicator (only fetch once)
if (players.length === 0) {
    fetch('/get-players')
        .then(response => response.json())
        .then(data => {
            players = data;  // Cache the players array
            currentPlayer = 0;  // Initialize to the first player
            updatePlayerTurn();  // Update the player turn
            console.debug('Players:', players);
        })
        .catch(error => console.error('Error fetching players:', error));
} /*else {
    updatePlayerTurn();  // Use the cached players if they exist
}*/

// Update the player turn indicator
function updatePlayerTurn() {
    if (players.length > 0) {
        document.getElementById('player-bar').textContent = `${players[currentPlayer]}'s Turn`;
    }
}

// Handle the dice roll
document.getElementById('roll-dice-btn').addEventListener('click', function () {
    fetch('/roll-dice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('dice-display').textContent = `🎲 ${data.green}, 🎲 ${data.red}`;
        updateHerd(data.player_herd, 'player-herd');
        updateHerd(data.main_herd, 'main-herd');

        // Update the current player based on the backend response
        currentPlayer = data.current_player_index;

        console.debug('Current Player:', currentPlayer);
        updatePlayerTurn();  // Update the player turn UI
    })
    .catch(error => console.error('Error during dice roll:', error));
});


// Ensure modal is initialized with correct content
function initializeModal() {
    const exchangeWith = document.getElementById('exchange-with').value;
    toggleExchangeMode(exchangeWith);  // Ensure correct section is shown when modal opens
}
// Handle change on the modal
document.getElementById('exchange-with').addEventListener('change', function() {
    const selectedValue = this.value;
    const indicator = document.getElementById('selected-value-indicator');

    // Update the indicator's text based on the selected value
    if (selectedValue === 'main-herd') {
        indicator.textContent = 'Selected: Main Herd';
    } else if (selectedValue === 'players') {
        indicator.textContent = 'Selected: Players';
    }
});

// Handle the exchange modal open/close
document.getElementById('make-exchange-btn').addEventListener('click', function() {
    document.getElementById('exchange-modal').style.display = 'block';
    initializeModal();  // Initialize the modal content when it's opened
});

document.getElementById('cancel-exchange').addEventListener('click', function() {
    document.getElementById('exchange-modal').style.display = 'none';
});

// Toggle between Main Herd and Player exchange when dropdown value changes
document.getElementById('exchange-with').addEventListener('change', function() {
    toggleExchangeMode(this.value);  // Pass the new value and update the sections
});

// Function to toggle modal sections based on the selected exchange option
function toggleExchangeMode(exchangeWith) {
    const mainHerdSection = document.getElementById('main-herd-exchange');
    const playerExchangeSection = document.getElementById('player-exchange');

    if (exchangeWith === 'main-herd') {
        mainHerdSection.style.display = 'block';
        playerExchangeSection.style.display = 'none';
    } else {
        mainHerdSection.style.display = 'none';
        playerExchangeSection.style.display = 'block';
    }
}

// Handle the submission of the exchange
document.getElementById('submit-exchange').addEventListener('click', function() {
    const exchangeWith = document.getElementById('selected-value-indicator').textContent;
    console.debug('Exchange With:', exchangeWith);
    let payload = { player_index: currentPlayer };  // Ensure currentPlayer is correctly set

    if (exchangeWith === 'Selected: Main Herd') {
        const selectedRatio = document.querySelector('input[name="exchange-ratio"]:checked');
        if (selectedRatio) {
            const [giveAnimal, receiveAnimal] = selectedRatio.value.split('-');
            const [giveCount, receiveCount] = selectedRatio.getAttribute('data-ratio').split('-');
            console.debug('Current Player:', currentPlayer);
            console.debug('Selected Ratio:', selectedRatio.value);
            console.debug('Give Animal:', giveAnimal, 'Receive Animal:', receiveAnimal);
            console.debug('Give Count:', giveCount, 'Receive Count:', receiveCount);

            payload.give_animal = giveAnimal;
            payload.receive_animal = receiveAnimal;
            payload.give_count = giveCount;
            payload.receive_count = receiveCount;
            payload.recipient = 'main-herd';
        } else {
            alert('Please select a valid exchange option.');
            return;
        }
    } else {
        const giveAnimal = document.getElementById('give-animal').value;
        const giveCount = document.getElementById('give-count').value;
        const receiveAnimal = document.getElementById('receive-animal').value;
        const receiveCount = document.getElementById('receive-count').value;
        console.debug('Give Animal:', giveAnimal, 'Give Count:', giveCount);
        console.debug('Receive Animal:', receiveAnimal, 'Receive Count:', receiveCount);

        payload.give_animal = giveAnimal;
        payload.give_count = giveCount;
        payload.receive_animal = receiveAnimal;
        payload.receive_count = receiveCount;
    }

    sendExchangeRequest('/post-exchange-request', payload);
    document.getElementById('exchange-modal').style.display = 'none';
});

// Function to send the exchange request
function sendExchangeRequest(url, payload) {
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Exchange completed!");
            updateHerd(data.player_herd, 'player-herd');  // Update player's herd
            updateHerd(data.main_herd, 'main-herd');      // Update main herd
            if (payload.recipient !== 'main-herd') {
                refreshPendingRequests();  // Refresh pending requests if necessary
            }
        } else {
            alert("Exchange failed.");
        }
    })
    .catch(error => console.error('Error processing exchange:', error));
}

// Function to update the herd display
function updateHerd(herdData, herdElementId) {
    const herdElement = document.getElementById(herdElementId);
    for (const animal in herdData) {
        const animalCountElement = herdElement.querySelector(`.animal-tile img[alt="${animal}"]`).nextElementSibling;
        animalCountElement.textContent = herdData[animal];
    }
}
// Initialize the game manager on page load
document.getElementById('forfeit-btn').addEventListener('click', function() {
    resetGameManager();
    // go to main menu page '/'
    window.location.href = '/';
});


