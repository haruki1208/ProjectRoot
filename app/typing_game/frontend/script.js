
// window.locationを使用して現在のホストとポート番号を取得
const host = window.location.hostname || '127.0.0.1';
const port = window.location.port || '5000';

// PythonサーバーのエンドポイントURLを動的に構築
const url = `http://${host}:${port}`;

// ウィンドウが閉じられる際に実行される関数
window.addEventListener('unload', function() {
    navigator.sendBeacon(url+'/close', '');
});

// ページが読み込まれた際にユーザー名を取得する関数を実行
window.onload = function() {
    getUserNamesFromServer();
};

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
    getUserNamesFromServer();
}

// 登録せずにホーム画面に戻る
function goBackToHome() {
    hideRegistrationScreen();
}

// ホーム画面に登録済みのユーザー名を表示するために取得
// function displayMemos() {
//     fetch(url+'/get_user_names')
//     .then(response => response.json())
//     .then(data => {
//         memosList.innerHTML = '';
//         data.forEach(memo => {
//             const listItem = document.createElement('li');
//             listItem.textContent = `ID: ${memo.id}, Tag: ${memo.tag}, Sentence: ${memo.sentence}, Date: ${memo.date}`;
//             memosList.appendChild(listItem);
//         });
//     })
//     .catch(error => console.error('Error fetching memos:', error));
// }


// ユーザ名を取得する関数
function getUserNamesFromServer() {
    // XMLHttpRequestオブジェクトを作成
    var xhr = new XMLHttpRequest();

    // GETリクエストを発行
    xhr.open('GET', url+'/get_user_names', true);

    // レスポンスが返ってきた時の処理
    xhr.onload = function () {
        if (xhr.status === 200) {
            // サーバーから取得したデータをJSON形式からJavaScriptオブジェクトに変換
            var response = JSON.parse(xhr.responseText);

            // ユーザーリストを取得してプルダウンリストに表示
            var userSelect = document.getElementById("userSelect");
            userSelect.innerHTML = '<option value="">選択してください</option>'; // 初期オプションを追加
            response.forEach(function (user) {
                var option = document.createElement("option");
                option.value = user;
                option.text = user;
                userSelect.appendChild(option);
            });
        }
    };

    // リクエストを送信
    xhr.send();
}


////////////////////////
// ユーザー登録関連
////////////////////////
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
            clearusernameInput();
            // ユーザー登録が完了したら、ホーム画面に戻る
            hideRegistrationScreen();
        });
    } else {
        alert('ユーザー名を入力してください。');
    }
}

// ユーザ名入力欄をクリアする
function clearusernameInput() {
    document.getElementById('usernameInput').value = '';
}



/////////////////////
// ゲーム関連
/////////////////////

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

// サーバーから単語を全部取得する関数
function fetchWords() {
    // サーバーから単語を取得する関数（バックエンドとの通信）
    // getRandomWord()
    // ここではサンプルとして固定の単語リストを使用します
    words = ['こんにちは', 'ありがとう', 'さようなら', 'おはよう', 'おやすみ'];
}

// 単語表示関数
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

// ゲームスタート
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

// ゲーム終了
function endGame() {
    document.getElementById('result').textContent = `結果: ${score} タイプ`;
    document.getElementById('homeScreen').style.display = 'block';
    document.getElementById('gameScreen').style.display = 'none';
    // サーバーにスコアを送信する関数（バックエンドとの通信）
    // ここではサンプルとして送信しないで表示のみ行います
}




