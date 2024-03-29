import { MongoClient } from "mongodb";
import { SimData } from "./types";

const DB_URI = "mongodb://admin:admin@mongo:3001";

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

export async function getLatest(collection_name : string) : Promise<SimData | null> {
    await clientPromise;
    let cursor = client.db("simulationdb").collection(collection_name).find({}).sort({_id: -1}).limit(1);
    let arr = await cursor.toArray()
    let doc = (arr.length > 0) ? arr[0] : null
    cursor.close()
    if (doc) {
        return {
            time_current: doc.time_current,
            time_delta: doc.time_delta,
            time_zero: doc.time_zero,
            reproduction_count: doc.reproduction_count,
            board: doc.board,
        }
    }
    return null
}

export async function getSpecific(collection_name : string, time : number) {
    await clientPromise;
    let cursor = client.db("simulationdb").collection(collection_name).find({time_current : time});
    let arr = await cursor.toArray();
    let doc = (arr.length > 0) ? arr[0] : null
    cursor.close()
    if (doc) {
        return {
            time_current: doc.time_current,
            time_delta: doc.time_delta,
            time_zero: doc.time_zero,
            reproduction_count: doc.reproduction_count,
            board: doc.board,
        }
    }
    return null
}