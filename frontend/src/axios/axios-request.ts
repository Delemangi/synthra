import axios from "axios";

export async function getFilesForSpecifiedUser(accessToken: string | null) : Promise<File[]>
{
    return await axios.get('http://localhost:8002/files', {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    }).then(response => {
      return response.data;
    }).catch(error => {
      console.log(error);
    });
}

export function sendFileForSpecifiedUser(accessToken: string | null, file: File) : void
{
    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:8002/files', formData, {
      headers: {
        authorization: `Bearer ${accessToken}`
      }
    }).then(response => {
      console.log(response);
    }).catch(error => {
      console.log(error);
    });
}
