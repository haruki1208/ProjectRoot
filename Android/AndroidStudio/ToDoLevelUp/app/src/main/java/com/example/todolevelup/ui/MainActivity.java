package com.example.todolevelup.ui;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import android.widget.TextView;

import com.example.todolevelup.R;
import com.example.todolevelup.model.Task;

import com.example.todolevelup.util.TaskStorage;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;


public class MainActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private TaskAdapter taskAdapter;
    private List<Task> taskList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView dateTextView = findViewById(R.id.dateTextView);
        String todayText = getFormattedDate();
        dateTextView.setText(todayText);


        recyclerView = findViewById(R.id.taskRecyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // 保存されたタスクリストを読み込む
        taskList = TaskStorage.loadTasks(this);
        if (taskList == null || taskList.isEmpty()) {
            taskList = createSampleTasks(); // 初回だけサンプルを表示
        }


        taskAdapter = new TaskAdapter(this, taskList);
        recyclerView.setAdapter(taskAdapter);
    }

    private String getFormattedDate() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy年 M月 d日 (E)", Locale.JAPANESE);
        return sdf.format(new Date());
    }


    private List<Task> createSampleTasks() {
        List<Task> list = new ArrayList<>();
        Date today = new Date();

        // 空のタスクを1つだけ追加（インデント0、親なし）
        Task emptyTask = new Task("", false, 0, null, today);
        list.add(emptyTask);

        return list;
    }
}
