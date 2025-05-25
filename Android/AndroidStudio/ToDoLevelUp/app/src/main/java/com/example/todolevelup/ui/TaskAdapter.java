package com.example.todolevelup.ui;

import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Button;
import android.widget.ImageButton;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Context;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.todolevelup.R;
import com.example.todolevelup.model.Task;
import com.example.todolevelup.util.TaskStorage;

import java.util.Date;
import java.util.List;

public class TaskAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {

    private static final int VIEW_TYPE_TASK = 0;
    private static final int VIEW_TYPE_ADD_BUTTON = 1;

    private List<Task> taskList;

    private Context context;

    public TaskAdapter(Context context, List<Task> taskList) {
        this.context = context;
        this.taskList = taskList;
    }


    @Override
    public int getItemViewType(int position) {
        return position == taskList.size() ? VIEW_TYPE_ADD_BUTTON : VIEW_TYPE_TASK;
    }

    @Override
    public int getItemCount() {
        return taskList.size() + 1; // 最後に追加ボタン用ビュー
    }

    @NonNull
    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if (viewType == VIEW_TYPE_TASK) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_task, parent, false);
            return new TaskViewHolder(view);
        } else {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_add_task, parent, false);
            return new AddButtonViewHolder(view);
        }
    }

    @Override
    public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
        if (holder instanceof TaskViewHolder) {
            Task task = taskList.get(position);
            TaskViewHolder vh = (TaskViewHolder) holder;

            vh.editText.setText(task.getText());
            vh.checkBox.setChecked(task.isChecked());

            vh.checkBox.setOnCheckedChangeListener((buttonView, isChecked) -> task.setChecked(isChecked));

            vh.editText.addTextChangedListener(new TextWatcher() {
                @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
                @Override public void onTextChanged(CharSequence s, int start, int before, int count) {}
                @Override public void afterTextChanged(Editable s) {
                    task.setText(s.toString());
                }
            });

            vh.deleteButton.setOnClickListener(v -> {
                int pos = holder.getAdapterPosition();
                new AlertDialog.Builder(holder.itemView.getContext())
//                    .setTitle("タスクの削除")
                    .setMessage("「" + task.getText() + "」を削除しますか？")
                    .setPositiveButton("削除", (dialog, which) -> {
                        taskList.remove(pos);
                        notifyItemRemoved(pos);
                        notifyItemRangeChanged(pos, taskList.size());
                        TaskStorage.saveTasks(context, taskList);
                    })
                    .setNegativeButton("キャンセル", null)
                    .show();
            });

        } else if (holder instanceof AddButtonViewHolder) {
            ((AddButtonViewHolder) holder).addButton.setOnClickListener(v -> {
                taskList.add(new Task("", false, 0, null, new Date()));
                notifyItemInserted(taskList.size() - 1);
                TaskStorage.saveTasks(context, taskList);
            });
        }
    }

    public static class TaskViewHolder extends RecyclerView.ViewHolder {
        CheckBox checkBox;
        EditText editText;
        ImageButton deleteButton;

        public TaskViewHolder(@NonNull View itemView) {
            super(itemView);
            checkBox = itemView.findViewById(R.id.taskCheckBox);
            editText = itemView.findViewById(R.id.taskEditText);
            deleteButton = itemView.findViewById(R.id.deleteButton);
        }
    }

    public static class AddButtonViewHolder extends RecyclerView.ViewHolder {
        Button addButton;

        public AddButtonViewHolder(@NonNull View itemView) {
            super(itemView);
            addButton = itemView.findViewById(R.id.addTaskButton);
        }
    }
}

