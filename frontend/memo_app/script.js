document.addEventListener('DOMContentLoaded', () => {
    const addMemoBtn = document.getElementById('addMemoBtn');
    const memosList = document.getElementById('memosList');

    // window.locationを使用して現在のホストとポート番号を取得
    const host = window.location.hostname || 'localhost';
    const port = window.location.port || '5000';
    
    // PythonサーバーのエンドポイントURLを動的に構築
    const url = `http://${host}:${port}/api/memos`;
    // console.log(url)

    // メモの一覧を取得して表示する関数
    function displayMemos() {
        fetch(url)
        .then(response => response.json())
        .then(data => {
            memosList.innerHTML = '';
            data.forEach(memo => {
                const listItem = document.createElement('li');
                listItem.textContent = `ID: ${memo.id}, Tag: ${memo.tag}, Sentence: ${memo.sentence}, Date: ${memo.date}`;
                memosList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching memos:', error));
    }

    // ページロード時にメモの一覧を表示
    displayMemos();

    // メモの追加ボタンがクリックされたときの処理
    addMemoBtn.addEventListener('click', () => {
        const tag = document.getElementById('tag').value;
        const sentence = document.getElementById('sentence').value;

        // メモを追加するためのリクエストを送信
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tag, sentence })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // メモの追加が成功したら、メモの一覧を更新して表示
            displayMemos();
        })
        .catch(error => console.error('Error adding memo:', error));
    });
});

