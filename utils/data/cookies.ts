import Cookies from "universal-cookie";

export const getToken = () => {
    const cookies = new Cookies();
    const token = cookies.get('token');

    return token;
};
  
export const getUserEmail = () => {
    const cookies = new Cookies();
    const userEmail = cookies.get('userEmail');

    return userEmail;
};