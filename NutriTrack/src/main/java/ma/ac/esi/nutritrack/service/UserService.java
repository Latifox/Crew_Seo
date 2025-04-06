package ma.ac.esi.nutritrack.service;

import ma.ac.esi.nutritrack.repository.UserRepository;

public class UserService {

    private final UserRepository userRepository;

    public UserService() {
        this.userRepository = new UserRepository();
    }

    public boolean findUserByCredentials(String login, String password) {

        return userRepository.userExists(login, password);
    }
}