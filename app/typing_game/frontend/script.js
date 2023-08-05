//////////////////////////
// 変数定義
//////////////////////////

let selectedUserName = '';      // ログイン中のユーザー名
let selectedGenreName = '';     // 選択中のジャンル名

/////////////////////////
// 汎用
/////////////////////////

// window.locationを使用して現在のホストとポート番号を取得
const host = window.location.hostname || '127.0.0.1';
const port = window.location.port || '5000';

// PythonサーバーのエンドポイントURLを動的に構築
const url = `http://${host}:${port}`;

// ウィンドウが閉じられる際に実行される関数
window.addEventListener('unload', function() {
    navigator.sendBeacon(url+'/close', '');
});

// 入力欄をクリアする
function clearInput(inputId) {
    document.getElementById(inputId).value = '';
}

// 画面から値を取得する関数
function getSelectedValue(selectElement, message) {
    const selectUser = document.getElementById(selectElement);
    const selectedValue = selectUser.value;

    // ゲームを開始する前に値が選択されているかを確認
    if (selectedValue === '') {
        alert(message);
        return;
    }

    return selectedValue;
}

/////////////////////////
// 画面関連
/////////////////////////

// ホーム → ユーザー登録画面
function showRegistrationScreen() {
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById('registrationScreen').style.display = 'block';
}

// ユーザー登録画面 → ホーム画面
function hideRegistrationScreen() {
    document.getElementById('registrationScreen').style.display = 'none';
    document.getElementById('homeScreen').style.display = 'block';
    getDataFromServer('/get_user_names',selectUser);
}

// 登録せずにホーム画面に戻る
function goBackToHome() {
    hideRegistrationScreen();
}

// ホーム画面 → ゲーム画面
function showGameScreen() {
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'block';
}

// ゲーム画面 → ホーム画面
function hideGameScreen() {
    document.getElementById('gameScreen').style.display = 'none';
    document.getElementById('homeScreen').style.display = 'block';
}

////////////////////////
// ユーザー関連
////////////////////////
// サーバーからデータを取得しプルダウンリストに表示する関数
function getDataFromServer(endpoint, selectElement) {
    // XMLHttpRequestオブジェクトを作成
    var xhr = new XMLHttpRequest();

    // GETリクエストを発行
    xhr.open('GET', url + endpoint, true);

    // レスポンスが返ってきた時の処理
    xhr.onload = function () {
        if (xhr.status === 200) {
            // サーバーから取得したデータをJSON形式からJavaScriptオブジェクトに変換
            var response = JSON.parse(xhr.responseText);

            // プルダウンリストに表示
            selectElement.innerHTML = '<option value="">選択してください</option>'; // 初期オプションを追加
            response.forEach(function (item) {
                var option = document.createElement("option");
                option.value = item;
                option.text = item;
                selectElement.appendChild(option);
            });
        }
    };

    // リクエストを送信
    xhr.send();
}


// ページが読み込まれた際
window.onload = function() {
    getDataFromServer('/get_user_names',selectUser);    // ユーザー名を取得する関数を実行
    getDataFromServer('/get_genre_names',selectGenre);  // ジャンルを取得する関数を実行
};

// ユーザー登録関数
function registerUser() {
    const username = document.getElementById('usernameInput').value.trim();
    if (username !== '') {
        // サーバーにユーザー名を送信するリクエスト
        fetch(url+'/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "username": username }) // ユーザー名をオブジェクトとして送信
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.username);
            clearInput('usernameInput');
            // ユーザー登録が完了したら、ホーム画面に戻る
            hideRegistrationScreen();
        });
    } else {
        alert('ユーザー名を入力してください。');
    }
}

/////////////////////
// ゲーム関連
/////////////////////

// ゲームスタート
function startGame() {
    const selectedUserName = getSelectedValue("selectUser","ユーザーを選択してください。");
    // ユーザーが選択されていない場合、ゲーム画面への遷移を中止
    if (!selectedUserName) {
        return; // 選択されていない場合、ここで処理を終了
    }
    document.getElementById('selectedUserNameDisplay').textContent = selectedUserName;
    const selectedGenreName = getSelectedValue("selectGenre","ジャンルを選択してください。");
    // ジャンルが選択されていない場合、ゲーム画面への遷移を中止
    if (!selectedGenreName) {
        return; // 選択されていない場合、ここで処理を終了
    }
    document.getElementById('selectedGenreNameDisplay').textContent = selectedGenreName;
    clearInput('userInput');
    // ここで選択したジャンルの単語を取得する
    getWordsFromGenre(selectedGenreName);
    // 次にランダムで一単語取得して表示する
    showGameScreen();
    setTimeout(() => {
        endGame();
    }, 180000); // 3分後にゲーム終了
}

// ゲーム終了
function endGame() {
    hideGameScreen();
    // サーバーにスコアを送信する関数（バックエンドとの通信）
}

// script.js

// 選択したジャンルの単語を取得して表示する
function getWordsFromGenre(selectedGenreName) {
    // サーバーにジャンル名を送信するリクエスト
    fetch(url+'/get_words', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "selectedGenreName": selectedGenreName })
    })
    .then(response => response.json())
    .then(data => displayWords(data.words))
    .catch(error => console.error('Error:', error));
}

// 取得した単語をランダムに表示する
function displayWords(words) {
    const wordDisplay = document.getElementById('wordDisplay');
    wordDisplay.innerHTML = ''; // 一度表示をクリア

    if (words.length === 0) {
        wordDisplay.innerText = 'No words found for the selected genre.';
        return;
    }

    // ランダムに単語を表示
    const randomIndex = Math.floor(Math.random() * words.length);
    const randomWord = words[randomIndex];
    wordDisplay.innerText = randomWord;
}


// ランダムにワードを取得する
// async function getRandomWord() {
//     const response = await fetch(url+'/get_random_word');
//     const data = await response.json();
//     return data.word;
// }

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

// let words = [];
// let currentIndex = 0;
// let score = 0;

// サーバーから単語を全部取得する関数
// function fetchWords() {
//     // サーバーから単語を取得する関数（バックエンドとの通信）
//     // getRandomWord()
//     // ここではサンプルとして固定の単語リストを使用します
//     words = ['こんにちは', 'ありがとう', 'さようなら', 'おはよう', 'おやすみ'];
// }

// 単語表示関数
// function displayWord() {
//     document.getElementById('wordDisplay').textContent = words[currentIndex];
//     // ここで対応するローマ字も表示する処理を追加
// }

// 入力されたローマ字をチェック
// function checkWord() {
//     const userInput = document.getElementById('userInput').value.trim().toLowerCase();
//     const currentWord = words[currentIndex].toLowerCase();

//     if (userInput === currentWord) {
//         score++;
//         document.getElementById('score').textContent = score;
//         currentIndex++;

//         if (currentIndex < words.length) {
//             displayWord();
//             document.getElementById('userInput').value = '';
//         } else {
//             endGame();
//         }
//     }
// }
