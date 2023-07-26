
// window.locationを使用して現在のホストとポート番号を取得
const host = window.location.hostname || '127.0.0.1';
const port = window.location.port || '5000';

// PythonサーバーのエンドポイントURLを動的に構築
const url = `http://${host}:${port}`;

// ウィンドウが閉じられる際に実行される関数
window.addEventListener('unload', function() {
    navigator.sendBeacon(url+'/close', '');
});

// ランダムにワードを取得する
async function getRandomWord() {
    const response = await fetch(url+'/get_random_word');
    const data = await response.json();
    return data.word;
}

// // 次の単語ランダム取得関数から取り出して表示関数にいれる
// async function nextWord() {
//     const word = await getRandomWord();
//     updateWordDisplay(word);
// }

// // ゲーム終了関数
// function endGame() {
//     clearInterval(timer);
//     gameRunning = false;
//     const userTyped = userInput.value.length;
//     saveGameResult(userTyped);
//     alert('ゲーム終了！あなたのタイピング数：' + userTyped);
// }

// // タイピング数をカウント
// async function saveGameResult(typedCount) {
//     const response = await fetch(url+'/save_game_result', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ count: typedCount })
//     });
//     const data = await response.json();
//     console.log(data.message);
// }

let words = [];
let currentIndex = 0;
let score = 0;

function fetchWords() {
    // サーバーから単語を取得する関数（バックエンドとの通信）
    // getRandomWord()
    // ここではサンプルとして固定の単語リストを使用します
    words = ['こんにちは', 'ありがとう', 'さようなら', 'おはよう', 'おやすみ'];
}

function displayWord() {
    document.getElementById('wordDisplay').textContent = words[currentIndex];
    // ここで対応するローマ字も表示する処理を追加
}

// 入力されたローマ字をチェック
function checkWord() {
    const userInput = document.getElementById('userInput').value.trim().toLowerCase();
    const currentWord = words[currentIndex].toLowerCase();

    if (userInput === currentWord) {
        score++;
        document.getElementById('score').textContent = score;
        currentIndex++;

        if (currentIndex < words.length) {
            displayWord();
            document.getElementById('userInput').value = '';
        } else {
            endGame();
        }
    }
}

function startGame() {
    fetchWords();
    currentIndex = 0;
    score = 0;
    displayWord();
    document.getElementById('userInput').value = '';
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';

    setTimeout(() => {
        endGame();
    }, 180000); // 3分後にゲーム終了
}

function endGame() {
    document.getElementById('result').textContent = `結果: ${score} タイプ`;
    document.getElementById('homeScreen').style.display = 'block';
    document.getElementById('gameScreen').style.display = 'none';
    // サーバーにスコアを送信する関数（バックエンドとの通信）
    // ここではサンプルとして送信しないで表示のみ行います
}

function showRegistrationScreen() {
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById('registrationScreen').style.display = 'block';
}

function registerUser() {
    const username = document.getElementById('usernameInput').value.trim();

    if (username !== '') {
        // サーバーにユーザー登録情報を送信する関数（バックエンドとの通信）
        // ここではサンプルとして送信しないで画面遷移のみ行います
        document.getElementById('homeScreen').style.display = 'block';
        document.getElementById('registrationScreen').style.display = 'none';
        document.getElementById('userSelect').innerHTML += `<option value="${username}">${username}</option>`;
    }
}
