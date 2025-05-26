package com.example.todolevelup.ui;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.ItemTouchHelper;

import com.example.todolevelup.R;
import com.example.todolevelup.model.Task;
import com.example.todolevelup.util.TaskStorage;

import java.text.SimpleDateFormat;
import java.util.*;

public class MainActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private TaskAdapter taskAdapter;
    private List<Task> allTasks = new ArrayList<>();
    private List<Task> displayList = new ArrayList<>();

    // --- 表示用のフラットリストを生成するロジック ---
    private List<Task> buildDisplayList(List<Task> allTasks) {
        List<Task> result = new ArrayList<>();
        buildChildrenRecursive(null, allTasks, result);
        return result;
    }

    private void buildChildrenRecursive(String parentId, List<Task> allTasks, List<Task> result) {
        for (Task task : allTasks) {
            if ((parentId == null && task.getParentId() == null) ||
                    (parentId != null && parentId.equals(task.getParentId()))) {
                result.add(task);
                buildChildrenRecursive(task.getId(), allTasks, result);
            }
        }
    }

    private String getFormattedDate() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy年 M月 d日 (E)", Locale.JAPANESE);
        return sdf.format(new Date());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView dateTextView = findViewById(R.id.dateTextView);
        dateTextView.setText(getFormattedDate());

        recyclerView = findViewById(R.id.taskRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        allTasks = TaskStorage.loadTasks(this);
        if (allTasks == null || allTasks.isEmpty()) {
            allTasks = new ArrayList<>();
            allTasks.add(new Task("", false, null, new Date())); // 初期タスク
        }

        displayList = buildDisplayList(allTasks);
        taskAdapter = new TaskAdapter(this, allTasks, displayList);
        recyclerView.setAdapter(taskAdapter);

        // --- スワイプによる階層変更処理 ---
        ItemTouchHelper itemTouchHelper = new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0, ItemTouchHelper.RIGHT | ItemTouchHelper.LEFT) {
            @Override
            public boolean onMove(RecyclerView rv, RecyclerView.ViewHolder vh, RecyclerView.ViewHolder target) {
                return false;
            }

            @Override
            public void onSwiped(RecyclerView.ViewHolder viewHolder, int direction) {
                int position = viewHolder.getAdapterPosition();
                if (position < 0 || position >= displayList.size()) return;

                Task current = displayList.get(position);

                if (direction == ItemTouchHelper.RIGHT) {
                    // 現在のタスクのインデント（階層）を計算
                    int currentIndent = getIndentLevel(current);
                    // 直前の同じ階層のタスクを探してそのIDを親にする
                    for (int i = position - 1; i >= 0; i--) {
                        Task candidate = displayList.get(i);
                        int candidateIndent = getIndentLevel(candidate);

                        if (candidateIndent == currentIndent) {
                            // 同じ階層の直前タスク → その子になる
                            current.setParentId(candidate.getId());
                            break;
                        } else if (candidateIndent < currentIndent) {
                            // 一つ上の階層のタスクが現れたらそこで終わり（親が見つからなかった）
                            break;
                        }
                    }

                } else if (direction == ItemTouchHelper.LEFT) {
                    // 親の親を新しい親にする
                    Task parent = findTaskById(current.getParentId());
                    if (parent != null) {
                        current.setParentId(parent.getParentId());
                    } else {
                        current.setParentId(null);
                    }
                }

                // リスト再構築して更新
                displayList = buildDisplayList(allTasks);
                taskAdapter.setDisplayList(displayList);
                taskAdapter.notifyDataSetChanged();
                TaskStorage.saveTasks(MainActivity.this, allTasks);
            }
        });

        itemTouchHelper.attachToRecyclerView(recyclerView);
    }

    private Task findTaskById(String id) {
        for (Task task : allTasks) {
            if (task.getId().equals(id)) {
                return task;
            }
        }
        return null;
    }
    private int getIndentLevel(Task task) {
        int level = 0;
        String parentId = task.getParentId();
        while (parentId != null) {
            Task parent = findTaskById(parentId);
            if (parent == null) break;
            level++;
            parentId = parent.getParentId();
        }
        return level;
    }
}
