package com.example.todolevelup.model;

import java.util.Date;
import java.util.UUID;

public class Task {

    private String id;          // 一意なID
    private String parentId;    // 親タスクのID（nullなら親タスク）
    private String text;        // 内容
    private boolean isChecked;  // チェック状態
    private Date date;          // 所属日付

    public Task(String text, boolean isChecked, String parentId, Date date) {
        this.id = UUID.randomUUID().toString();
        this.text = text;
        this.isChecked = isChecked;
        this.parentId = parentId;
        this.date = date;
    }

    // --- Getter ---

    public String getId() {
        return id;
    }

    public String getParentId() {
        return parentId;
    }

    public String getText() {
        return text;
    }

    public boolean isChecked() {
        return isChecked;
    }


    public Date getDate() {
        return date;
    }

    // --- Setter ---
    public void setParentId(String parentId) {
        this.parentId = parentId;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void setChecked(boolean checked) {
        isChecked = checked;
    }

    public void setDate(Date date) {
        this.date = date;
    }
}
