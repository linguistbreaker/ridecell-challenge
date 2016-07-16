import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.concurrent.ArrayBlockingQueue;

public class Tail {

    public static void main(String[] args) throws IOException {
    // first arg should be a filename
    ArrayBlockingQueue q = new ArrayBlockingQueue(2);
    if(args.length == 0){
      System.err.println("Please provide at least a filename as an argument.");
    }else{
        try{
        BufferedReader br = new BufferedReader(new FileReader(args[0]));
        for (String line; (line = br.readLine()) != null;) {
            // System.out.print(line);
            // System.out.print('\n');
            if(q.offer(line)){
              }else{
                q.poll();
                q.offer(line);
              }
            }
        // Don't have to close the buffer 'cause modern niceties
        }catch(IOException excptn){
          System.err.println("Can't find that file. Maybe you misstyped the name or the path?");
        }
      }
      if(q.size() > 0){
        // System.out.print("And the last two lines were : \n");
        while(q.peek() != null){
          System.out.print(q.poll() + "\n");
        }
      }
    }
}
