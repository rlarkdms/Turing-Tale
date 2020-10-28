package com.example.hanium_aws;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferListener;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferNetworkLossHandler;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferState;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import java.io.File;
import java.io.InputStream;
import java.util.ArrayList;

//여기는 처음 부분 oncreate 부분 부터 작동하는 이미지 보여주고 지랄 났죠?

public class MainActivity extends AppCompatActivity {

    private static final int REQUEST_CODE = 0;
    private ImageView imageView;
    private TextView textview;
    private Button button;
    private EditText edittext;
    Bitmap img;
    Uri selectedImageURI;
    AmazonS3 s3;
    TransferUtility transferUtility;

    File file;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        edittext=findViewById(R.id.edit_text);
        imageView = findViewById(R.id.imageView);
        button=findViewById(R.id.upload_btn);

        tedPermission();//permission보여주는 부분 False 일때만 계속 보여주고 True되면  가능
         CognitoCachingCredentialsProvider credentialsProvider = new CognitoCachingCredentialsProvider(
                 getApplicationContext(),
                "us-east-1:17971bfd-0cd5-4f9b-8f3d-37f2bde670af", // Identity pool ID
                Regions.US_EAST_1 // Region
        );
         s3=new AmazonS3Client(credentialsProvider);
         s3.setRegion(Region.getRegion(Regions.US_EAST_1));
         s3.setEndpoint("s3.us-east-1.amazonaws.com");


        TransferNetworkLossHandler.getInstance(getApplicationContext());
         transferUtility=new TransferUtility(s3,getApplicationContext());

        imageView.setOnClickListener(new View.OnClickListener(){
            @RequiresApi(api = Build.VERSION_CODES.KITKAT)
            @Override
            public void onClick(View v) {

                Intent intent = new Intent();
                intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);
                //System.out.println("이거 값을 찾아야함"+intent.ACTION_GET_CONTENT);
                startActivityForResult(intent, REQUEST_CODE);
                //file = new File(getRealPathFromURI(selectedImageURI));
            }

        });

        button.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {//여기가 submit 부분

                TransferObserver observer=transferUtility.upload(
                        "textracttest7220",
                        String.valueOf(edittext.getText()+".jpg"),
                        file
                );

            }

        });

    }



    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    private String getRealPathFromURI(Uri contentUri) {
        if (contentUri.getPath().startsWith("/storage")) {
            return contentUri.getPath(); }
        String id = DocumentsContract.getDocumentId(contentUri).split(":")[1];
        String[] columns = { MediaStore.Files.FileColumns.DATA };
        String selection = MediaStore.Files.FileColumns._ID + " = " + id;
        Cursor cursor = getContentResolver().query(MediaStore.Files.getContentUri("external"), columns, selection, null, null);
        try { int columnIndex = cursor.getColumnIndex(columns[0]);
            if (cursor.moveToFirst()) {
                return cursor.getString(columnIndex);
            }
        } finally {
            cursor.close();
        }
        return null;
    }

//권한 요청 부분임.
    private void tedPermission() {

        PermissionListener permissionListener = new PermissionListener() {
            @Override
            public void onPermissionGranted() {
                // 권한 요청 성공

            }

            @Override
            public void onPermissionDenied(ArrayList<String> deniedPermissions) {
                android.os.Process.killProcess(android.os.Process.myPid());
                // 권한 요청 실패
            }
        };


        TedPermission.with(this)
                .setPermissionListener(permissionListener)
                .setPermissions(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                .check();
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE) {
            if (resultCode == RESULT_OK) {
                try {
                    InputStream in = getContentResolver().openInputStream(data.getData());

                    selectedImageURI =data.getData();
                    file=new File(getRealPathFromURI(selectedImageURI));
                    System.out.println("첫번째 부분까지 되는지 확인");
                    System.out.println(selectedImageURI);
                    img = BitmapFactory.decodeStream(in);
                    System.out.println("여기부분 확인해야함");
                    //System.out.print(imageFile);

                    in.close();

                    //img가 사진임 이 이미지를 업로드 해야함.

                    textview = findViewById(R.id.confirm);

                    System.out.print(img);
                    imageView.setImageBitmap(img);
                } catch (Exception e) {

                }
            } else if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, "사진 선택 취소", Toast.LENGTH_LONG).show();
            }
        }
    }
}
