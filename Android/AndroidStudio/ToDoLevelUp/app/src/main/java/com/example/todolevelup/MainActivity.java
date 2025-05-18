package com.example.todolevelup;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private TaskAdapter taskAdapter;
    private List<Task> taskList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recyclerView = findViewById(R.id.taskRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // 仮のタスクリスト作成
        taskList = createSampleTasks();

        taskAdapter = new TaskAdapter(taskList);
        recyclerView.setAdapter(taskAdapter);
    }

    private List<Task> createSampleTasks() {
        List<Task> list = new ArrayList<>();
        Date today = new Date();

        // 親タスク
        Task task1 = new Task("買い物リストを作成", false, 0, null, today);
        list.add(task1);

        // 子タスク（task1の子）
        Task task1_1 = new Task("・牛乳を買う", false, 1, task1.getId(), today);
        Task task1_2 = new Task("・卵を買う", false, 1, task1.getId(), today);
        list.add(task1_1);
        list.add(task1_2);

        // 別の親タスク
        Task task2 = new Task("仕事の資料準備", true, 0, null, today);
        list.add(task2);

        return list;
    }
}
