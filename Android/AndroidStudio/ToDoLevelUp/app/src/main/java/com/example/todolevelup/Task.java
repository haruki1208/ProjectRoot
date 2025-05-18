package com.example.todolevelup;

import java.util.Date;

import java.util.Date;
import java.util.UUID;

public class Task {

    private String id;          // 一意なID
    private String parentId;    // 親タスクのID（nullなら親タスク）
    private String text;        // 内容
    private boolean isChecked;  // チェック状態
    private int indentLevel;    // 表示インデント用（0＝親）
    private Date date;          // 所属日付

    public Task(String text, boolean isChecked, int indentLevel, String parentId, Date date) {
        this.id = UUID.randomUUID().toString();
        this.text = text;
        this.isChecked = isChecked;
        this.indentLevel = indentLevel;
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

    public int getIndentLevel() {
        return indentLevel;
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

    public void setIndentLevel(int indentLevel) {
        this.indentLevel = indentLevel;
    }

    public void setDate(Date date) {
        this.date = date;
    }
}
