//////////////////////////
// 変数定義
//////////////////////////

let selectedUserName = '';      // ログイン中のユーザー名
let selectedGenreName = '';     // 選択中のジャンル名
let userScore = 0;              // スコア
let endGameTimer = 0;           // 終了までの時間


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

// ホーム → 別画面
// 例) showAnotherScreen('gameScreen')
// 例) showAnotherScreen('registrationScreen')
// 例) showAnotherScreen('wordRegistrationScreen')
function showAnotherScreen(anotherScreen) {
    document.getElementById('homeScreen').style.display = 'none';
    document.getElementById(anotherScreen).style.display = 'block';
    getDataFromServer('/get_genre_names',existingGenre);  // 既存ジャンルを取得する関数を実行
}

// ホーム画面に戻る
function goBackToHome(currentScreen) {
    document.getElementById(currentScreen).style.display = 'none';
    document.getElementById('homeScreen').style.display = 'block';
    getDataFromServer('/get_user_names',selectUser);    // ユーザー名を取得する関数を実行
    getDataFromServer('/get_genre_names',selectGenre);  // ジャンルを取得する関数を実行
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
    const usernameInput = document.getElementById('usernameInput');
    const username = usernameInput.value.trim();
    
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
            if (data.message === "ユーザー登録が完了しました。") {
                clearInput('usernameInput');
                alert('ユーザー名「'+data.username+'」を登録しました。');
                // ユーザー登録が完了したら、ホーム画面に戻る
                goBackToHome('registrationScreen');
            } else if (data.message === "そのユーザー名は既に存在します。") {
                alert('「'+username+'」は既に登録されています。');
                clearInput('usernameInput');
            } else {
                alert('エラーが発生しました。');
            }
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

///////////////////////
// 単語登録関係
///////////////////////

// 既存ジャンルの単語を登録する関数
function registerExistingWord() {
    const selectedGenreName = getSelectedValue("existingGenre", "ジャンルを選択してください。");
    const existingWordInput = document.getElementById("existingWord");
    const existingWords = existingWordInput.value.split(','); // 入力された単語をカンマで分割
    
    // サーバーにデータを送信
    const requestData = {
        genre: selectedGenreName,
        words: existingWords // 複数の単語を配列として送信
    };

    fetch('/register_existing_words', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('単語が登録されました！');
            // 他の必要な処理を追加
        } else {
            alert('単語の登録に失敗しました。');
        }
    })
    .catch(error => {
        console.error('エラー:', error);
        alert('エラーが発生しました。');
    });
}

// 新規ジャンルと単語を登録する関数
function registerNewWord() {
    const newGenreName = getSelectedValue("newGenre", "ジャンルを入力してください。");
    const newWordInput = document.getElementById("newWord");
    const newWords = newWordInput.value.split(','); // 入力された単語をカンマで分割
    
    // サーバーにデータを送信
    const requestData = {
        genre: newGenreName,
        words: newWords // 複数の単語を配列として送信
    };

    fetch('/register_new_words', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('単語が登録されました！');
            // 他の必要な処理を追加
        } else {
            alert('単語の登録に失敗しました。');
        }
    })
    .catch(error => {
        console.error('エラー:', error);
        alert('エラーが発生しました。');
    });
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

    startCountdown(3,function() {
        document.getElementById('gameScreen').style.display = 'block';
        // ここで選択したジャンルの単語を取得する
        getWordsFromGenre(selectedGenreName, function(words) {
            // ゲームスタート時に単語リストを取得して、ゲームを開始
            playGame(words);
        });
        // ゲーム終了の自動タイマーをセット
        endGameTimer = setTimeout(() => {
            endGame();
        // }, 20000); // 20秒後にゲーム終了
        }, 180000); // 3分後にゲーム終了
    });
}

// カウントダウン後に関数を呼び出す
function startCountdown(second,callback) {
    const countdownDisplay = document.getElementById('countdownDisplay');
    document.getElementById('homeScreen').style.display = 'none';
    countdownDisplay.style.display = 'block';
    
    let countdown = second; // カウントダウン秒数
    countdownDisplay.textContent = countdown;
    
    const countdownInterval = setInterval(() => {
        countdown--;
        countdownDisplay.textContent = countdown;
        
        if (countdown === 0) {
            clearInterval(countdownInterval);
            countdownDisplay.style.display = 'none'; // カウントダウン非表示
            if (typeof callback === 'function') {
                callback(); // カウントダウン後に指定されたコールバックを実行
            }
        }
    }, 1000);
}

// ゲーム終了
function endGame() {
    // ユーザーのスコアをサーバーに送信
    console.log('userScore:'+userScore);
    saveUserScoreToServer(userScore);
    alert(selectedUserName+'さんのスコアは '+userScore+'です')
    goBackToHome('gameScreen');
    // タイマーをクリアして、自動終了を防ぐ
    clearTimeout(endGameTimer);
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
            userScore += currentWord.length;  // ゆくゆくはひらがなの文字数にする★
            userInput.value = ''; // 入力欄をクリア
            displayNextWord();
        }
    }

    // 最初の単語を表示
    displayNextWord();
}