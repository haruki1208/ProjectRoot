package com.example.todolevelup.util;

import android.content.Context;
import android.content.SharedPreferences;

import com.example.todolevelup.model.Task;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

public class TaskStorage {

    private static final String PREFS_NAME = "task_prefs";
    private static final String KEY_TASK_LIST = "task_list";

    public static void saveTasks(Context context, List<Task> tasks) {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        Gson gson = new Gson();
        String json = gson.toJson(tasks);
        editor.putString(KEY_TASK_LIST, json);
        editor.apply();
    }

    public static List<Task> loadTasks(Context context) {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        String json = prefs.getString(KEY_TASK_LIST, null);
        if (json == null) return new ArrayList<>();
        Gson gson = new Gson();
        Type type = new TypeToken<List<Task>>() {}.getType();
        return gson.fromJson(json, type);
    }
}
