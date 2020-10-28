package com.example.hanium_aws;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

public class introActivity extends Activity {
    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_intro);

        Handler handle = new Handler();

        handle.postDelayed(new Runnable() {

            public void run() {

                Intent intent = new Intent(introActivity.this, MainActivity.class);

                startActivity(intent);

                finish();

            }

        }, 1500);

    }
    @Override
    protected void onPause(){
        super.onPause();
        finish();
    }
}
