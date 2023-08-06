//////////////////////////
// 変数定義
//////////////////////////

let selectedUserName = '';      // ログイン中のユーザー名
let selectedGenreName = '';     // 選択中のジャンル名
let userScore = 0;              // スコア


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

// ユーザー名からidを取得する関数
async function getIdFromUser() {
    if (selectedUserName !== '') {
        try {
            const response = await fetch(url + '/get_id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "username": selectedUserName }) // ユーザー名をオブジェクトとして送信
            });
            
            const data = await response.json();
            const userId = data.userId;
            console.log('userId:' + data.userId);
            return userId;
        } catch (error) {
            console.error('エラーが発生しました:', error);
            // エラーハンドリングを行うか、適切な値を返す必要がある
        }
    } else {
        alert('選択されたユーザー名が登録されていません。');
        // エラーハンドリングを行うか、適切な値を返す必要がある
    }
}


/////////////////////
// ゲーム関連
/////////////////////

// ゲームスタート
function startGame() {
    selectedUserName = getSelectedValue("selectUser","ユーザーを選択してください。");
    console.log('username:'+selectedUserName);
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
    showGameScreen();
    // ここで選択したジャンルの単語を取得する
    getWordsFromGenre(selectedGenreName, function(words) {
        // ゲームスタート時に単語リストを取得して、ゲームを開始
        playGame(words);
    });
    setTimeout(() => {
        endGame();
    }, 20000); // 10秒後にゲーム終了
    // }, 180000); // 3分後にゲーム終了
}

// ゲーム終了
function endGame() {
    // ユーザーのスコアをサーバーに送信
    console.log('userScore:'+userScore);
    saveUserScoreToServer(userScore);
    hideGameScreen();
}

// 選択したジャンルの単語を取得して表示する
function getWordsFromGenre(selectedGenreName, callback) {
    // サーバーにジャンル名を送信するリクエスト
    fetch(url+'/get_words', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "selectedGenreName": selectedGenreName })
    })
    .then(response => response.json())
    .then(data => callback(data.words))
    .catch(error => console.error('Error:', error));
}

// サーバーにユーザーのスコアを送信する関数
async function saveUserScoreToServer(score) {
    try {
        const userId = await getIdFromUser(); // getIdFromUser関数が非同期関数になったことに注意

        console.log('username:' + selectedUserName);
        console.log('userId:' + userId);
        console.log('score:' + score);

        const data = {
            user_id: userId,
            score: score
        };

        const response = await fetch(url + '/save_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        // サーバーからのレスポンスを処理
        // alert(responseData.message);
        console.log(responseData.message); // メッセージを表示（必要に応じてアラートや別の表示方法に変更）
    } catch (error) {
        console.error('Error:', error);
    }
}

// ゲームをプレイする
function playGame(words) {
    const wordDisplay = document.getElementById('wordDisplay');
    const userInput = document.getElementById('userInput');

    function displayNextWord() {
        if (words.length === 0) {
            // ゲーム終了
            endGame();
            return;
        }

        // ランダムに単語を表示
        const randomIndex = Math.floor(Math.random() * words.length);
        const randomWord = words[randomIndex];

        wordDisplay.innerText = randomWord;
        // 一回出た単語はもう出ないようにする
        words.splice(randomIndex, 1);

        // ユーザーの入力をチェック
        userInput.oninput = checkWord;
    }

    // ユーザーの入力をチェック
    function checkWord() {
        const currentWord = wordDisplay.innerText.trim().toLowerCase();
        const inputWord = userInput.value.trim().toLowerCase();
        if (inputWord === currentWord) {
            userScore++;
            console.log('userScore:'+userScore)
            displayNextWord();
            userInput.value = ''; // 入力欄をクリア
        }
    }

    // 最初の単語を表示
    displayNextWord();
}