package com.example.todolevelup;

import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class TaskAdapter extends RecyclerView.Adapter<TaskAdapter.TaskViewHolder> {

    private List<Task> taskList;

    public TaskAdapter(List<Task> taskList) {
        this.taskList = taskList;
//        addEmptyTaskIfNeeded(); // 初期化時にも空白行を追加
    }

    public static class TaskViewHolder extends RecyclerView.ViewHolder {
        CheckBox checkBox;
        EditText editText;

        public TaskViewHolder(@NonNull View itemView) {
            super(itemView);
            checkBox = itemView.findViewById(R.id.taskCheckBox);
            editText = itemView.findViewById(R.id.taskEditText);
        }
    }

    @NonNull
    @Override
    public TaskViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_task, parent, false);
        return new TaskViewHolder(view);
    }

//    @Override
//    public void onBindViewHolder(@NonNull TaskViewHolder holder, int position) {
//        Task task = taskList.get(position);
//
//        holder.taskText.setText(task.getText());
//        holder.taskCheckBox.setChecked(task.isChecked());
//
//        // インデント（サブタスク）用の余白調整
//        ViewGroup.MarginLayoutParams params =
//                (ViewGroup.MarginLayoutParams) holder.taskText.getLayoutParams();
//        params.setMarginStart(task.getIndentLevel() * 40);
//        holder.taskText.setLayoutParams(params);
//
//        holder.taskText.setOnFocusChangeListener((v, hasFocus) -> {
//            if (hasFocus && task.getText().isEmpty()) {
//                // 空白行に入力が始まったら正式なタスクとして扱い、次の空白行を追加
//                task.setText(holder.taskText.getText().toString());
//                addEmptyTaskIfNeeded();
//            }
//        });
//    }
    @Override
    public void onBindViewHolder(@NonNull TaskViewHolder holder, int position) {
        Task task = taskList.get(position);

        // 表示内容を設定
        holder.checkBox.setChecked(task.isChecked());
        holder.editText.setText(task.getText());

        // インデント調整（階層に応じて左パディング）
        int padding = 50 * task.getIndentLevel(); // 1階層ごとに50px左に寄せる
        holder.itemView.setPadding(padding, holder.itemView.getPaddingTop(),
                holder.itemView.getPaddingRight(), holder.itemView.getPaddingBottom());

        // チェック状態の更新
        holder.checkBox.setOnCheckedChangeListener((buttonView, isChecked) -> {
            task.setChecked(isChecked);
        });

        // テキスト変更の反映
        holder.editText.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) {}
            @Override public void afterTextChanged(Editable s) {
                task.setText(s.toString());
            }
        });
    }

    @Override
    public int getItemCount() {
        return taskList.size();
    }
//    private void addEmptyTaskIfNeeded() {
//        // 最後のタスクが空白でないなら、空白タスクを追加
//        if (taskList.isEmpty() || !taskList.get(taskList.size() - 1).getText().isEmpty()) {
//            Task emptyTask = new Task("", false, 0, null, new Date());
//            taskList.add(emptyTask);
//            notifyItemInserted(taskList.size() - 1);
//        }
//    }

//    public static class TaskViewHolder extends RecyclerView.ViewHolder {
//        CheckBox taskCheckBox;
//        EditText taskText;
//
//        public TaskViewHolder(@NonNull View itemView) {
//            super(itemView);
//            taskCheckBox = itemView.findViewById(R.id.taskCheckBox);
//            taskText = itemView.findViewById(R.id.taskText);
//        }
//    }
}

