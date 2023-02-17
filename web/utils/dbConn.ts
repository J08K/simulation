import { MongoClient } from "mongodb";
import { SimData } from "./types";

const DB_URI = "mongodb://admin:admin@localhost:3001";

let client = new MongoClient(DB_URI, {});
let clientPromise = client.connect();


export async function checkStatus () {
    try {
        await clientPromise;
        await client.db("simulationdb").command({ping: 1})
        return true
    } catch (e) {
        console.log(e)
        return false
    }
}

export async function getCollections () {
    await clientPromise;
    let collection_names = await client.db("simulationdb").collections();
    let output : string[] = [];
    collection_names.forEach((collection) => {
        output.push(collection.collectionName)
    });
    return output
}

export async function getLatest(collection_name : string) {
    await clientPromise;
    let cursor = client.db("simulationdb").collection(collection_name).find({}).sort({_id: -1}).limit(1);
    let arr = await cursor.toArray()
    let doc = (arr.length > 0) ? arr[0] : null
    cursor.close()
    return doc
}