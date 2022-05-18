package Users;

public class User {

    private final String username;
    private final String password;
    private final String label; // client/artist
    private int userId;
    private int clientId;
    private int artistId;

    static User userInstance = null;

    private User(String username,String password,String label,int clientId, int artistId,int userId){
        this.username = username;
        this.password = password;
        this.label = label;
        this.userId = userId;
        this.clientId = clientId;
        this.artistId = artistId;
    }

    public static User getUserInstance(String username, String password, String label,int clientId, int artistId,int userId){
        if(userInstance == null){
            userInstance = new User(username,password,label,clientId,artistId,userId);
        }
        return userInstance;
    }

    public static User getUserInstance(){
        if (userInstance == null){
            return null;
        }
        return userInstance;
    }

    public static void deleteInstance(){
        userInstance = null;
    }

    public String getUsername() {
        return username;
    }

    public String getLabel() {
        return label;
    }

    public int getClientId() {
        return clientId;
    }

    public int getArtistId() {
        return artistId;
    }
}
