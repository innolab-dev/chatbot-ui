import Cookies from "universal-cookie";

export const getToken = () => {
    const cookies = new Cookies();
    const token = cookies.get('token');
    console.log("token", token);

    return token;
};
  
export const getUserEmail = () => {
    const cookies = new Cookies();
    const userEmail = cookies.get('userEmail');
    console.log("userEmail", userEmail);

    return userEmail;
};