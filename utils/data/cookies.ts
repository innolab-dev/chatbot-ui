import Cookies from "universal-cookie";

const cookies = new Cookies();
var email = "";
export const getToken = () => {
    const token = cookies.get('token');
    return token;
};
  
export const getCookieEmail = () => {
    const userEmail = cookies.get('userEmail');
    email = userEmail;
    return userEmail;
};

export const getUserEmail = () => {
    return email;
}