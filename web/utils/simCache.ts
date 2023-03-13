import type { SimData } from "./types";

function getNumDecimals(n : number) {
    return (n % 1).toString().substring(2).length;
}

function round(val : number, num_decimals : number) {
    return Math.round(val * Math.pow(10, num_decimals)) / Math.pow(10, num_decimals);
}

async function fetcher (url : string, params: RequestInit = {}) : Promise<SimData | null> {
    return fetch(url, params).then((res) => res.json()).then((data : {sim_data : SimData | null}) => data.sim_data);
}

export class SimDataCache {
    private size : number;
    private collection : string | null;

    private accuracy : number;
    private time_delta : number;

    private cache : Map<number, Promise<SimData | null>>;

    constructor (size : number) {
        this.size = size;
        this.collection = null;

        this.accuracy = 2; // For most cases this should be fine.
        this.time_delta = 0.01;

        this.cache = new Map();

        this.setAccuracy();
    }

    url(time : number) : string {
        return `http://localhost:3000/api/database/collections/${this.collection}/${time}`
    }

    setAccuracy() {
        fetcher(this.url(-1)).then((result) => {
            if (result) {
                this.time_delta = result.time_delta;
                this.accuracy = getNumDecimals(result.time_delta);
            }
        });
    }

    setCollection(collection : string | null) {
        this.collection = collection;
        this.cache = new Map();
    }

    async setCachedSims(time : number) {
        let low = time - Math.floor((this.size - 1) / 2) * this.time_delta;
        let high = time + Math.ceil((this.size - 1) / 2) * this.time_delta;

        // TODO Make this actually asyncronous.

        for (let idx=low; idx <= high; idx = round(idx + this.time_delta, this.accuracy)) {
            if (idx >= 0 && idx !== time && !this.cache.has(idx)) { // TODO Check if we can do this without the 'has()'. Might be slow? O(log(n))
                this.cache.set(idx, fetcher(this.url(round(idx, this.accuracy))));
            }
        }

        for (let [key, _] of this.cache.entries()) {
            if (key < low || key > high) {
                this.cache.delete(key);
            }
        }
    }

    async get(time : number) : Promise<SimData | null> {
        if (this.collection) {
            if (this.cache.has(time)) {
                let target = await this.cache.get(time);
                this.setCachedSims(time);
                return target ? target : null
            } else {
                let target = await fetcher(this.url(time));
                this.cache.set(time, new Promise(() => target));
    
                this.setCachedSims(time);
                return target
            }
        } else {
            console.error("Collection has not been set!");
            return null;
        }
    }

    length () {
        return this.cache.size;
    }
}