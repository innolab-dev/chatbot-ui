const { MongoClient } = require('mongodb');
// const MongoClient = require('mongodb').MongoClient;
// Replace with your actual MongoDB connection string 
const url = 'mongodb+srv://projectvpn39:kDir8fgavrwmXhUN@cluster0.bdqojht.mongodb.net/langchain?retryWrites=true&w=majority';

const client = new MongoClient(url);

async function main() {
  await client.connect();
  
  const db = client.db('langchain');
  
  const collection = db.collection('chat_history');
  user = await collection.findOne({ SessionId: "4111d3e1-4f55-46e7-9021-1974f98123d0" })
  console.log(user);
              // console.log(user.History);
              // response.json({ message: user.interest });
  // Use the collection as neede
  // console.log(collection.findOne
  //   ({"SessionId": "4111d3e1-4f55-46e7-9021-1974f98123d0"}))
  // await client.close();
}

main();