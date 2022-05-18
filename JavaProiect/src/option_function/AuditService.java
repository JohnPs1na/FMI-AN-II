package option_function;

import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class AuditService {
    FileWriter writer;
    String timeStamp;
    static AuditService instance = null;

    public void register(String action) throws IOException {
        writer.append(action);
        timeStamp = new SimpleDateFormat("yyyy-MM-dd_HH:mm:ss").format(Calendar.getInstance().getTime());
        writer.append(",");
        writer.append(timeStamp);
        writer.append("\n");
        writer.flush();
    }

    private AuditService(){
        try{
            this.writer = new FileWriter("data/auditLog.csv");
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    public static AuditService getInstance(){
        if (instance == null){
            instance = new AuditService();
        }
        return instance;
    }
}
