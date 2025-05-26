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

    private List<Task> allTasks;      // 全タスク（親子構造あり）
    private List<Task> displayList;   // 表示順にフラット展開されたタスク
    private Context context;

    public TaskAdapter(Context context, List<Task> allTasks, List<Task> displayList) {
        this.context = context;
        this.allTasks = allTasks;
        this.displayList = displayList;
    }

    @Override
    public int getItemCount() {
        return displayList.size() + 1; // 最後に追加ボタン用ビュー
    }

    @Override
    public int getItemViewType(int position) {
        return position == displayList.size() ? VIEW_TYPE_ADD_BUTTON : VIEW_TYPE_TASK;
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
            Task task = displayList.get(position);
            TaskViewHolder vh = (TaskViewHolder) holder;

            vh.editText.setText(task.getText());
            vh.checkBox.setChecked(task.isChecked());

            // --- ParentId をたどってインデントレベルを算出 ---
            int indentLevel = calculateIndentLevel(task);
            int indentPx = (int) (indentLevel * 32 * vh.itemView.getResources().getDisplayMetrics().density); // 32dp/階層
            vh.indentWrapper.setPadding(indentPx, 0, 0, 0);

            vh.checkBox.setOnCheckedChangeListener((buttonView, isChecked) -> {
                task.setChecked(isChecked);
                TaskStorage.saveTasks(context, allTasks);
            });

            vh.editText.addTextChangedListener(new TextWatcher() {
                @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
                @Override public void onTextChanged(CharSequence s, int start, int before, int count) {}
                @Override public void afterTextChanged(Editable s) {
                    task.setText(s.toString());
                }
            });

            vh.deleteButton.setOnClickListener(v -> {
                int pos = holder.getAdapterPosition();
                Task target = displayList.get(pos);
                new AlertDialog.Builder(holder.itemView.getContext())
                        .setMessage("「" + target.getText() + "」を削除しますか？")
                        .setPositiveButton("削除", (dialog, which) -> {
                            allTasks.remove(target);
                            displayList.remove(pos);
                            notifyItemRemoved(pos);
                            TaskStorage.saveTasks(context, allTasks);
                        })
                        .setNegativeButton("キャンセル", null)
                        .show();
            });

        } else if (holder instanceof AddButtonViewHolder) {
            ((AddButtonViewHolder) holder).addButton.setOnClickListener(v -> {
                Task newTask = new Task("", false, null, new Date());
                allTasks.add(newTask);
                displayList.add(newTask);
                notifyItemInserted(displayList.size() - 1);
                TaskStorage.saveTasks(context, allTasks);
            });
        }
    }

    private int calculateIndentLevel(Task task) {
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

    private Task findTaskById(String id) {
        for (Task t : allTasks) {
            if (t.getId().equals(id)) return t;
        }
        return null;
    }

    public void setDisplayList(List<Task> displayList) {
        this.displayList = displayList;
    }

    public static class TaskViewHolder extends RecyclerView.ViewHolder {
        CheckBox checkBox;
        EditText editText;
        ImageButton deleteButton;
        View indentWrapper;

        public TaskViewHolder(@NonNull View itemView) {
            super(itemView);
            checkBox = itemView.findViewById(R.id.taskCheckBox);
            editText = itemView.findViewById(R.id.taskEditText);
            deleteButton = itemView.findViewById(R.id.deleteButton);
            indentWrapper = itemView.findViewById(R.id.indentWrapper);
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


