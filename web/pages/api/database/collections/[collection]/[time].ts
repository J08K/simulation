import type { NextApiRequest, NextApiResponse } from 'next';
import type { SimData } from '@/utils/types';
import { getLatest, getSpecific } from '@/utils/dbConn';

type Data = {
    sim_data : SimData | null,
}

export default async function handler (
    req: NextApiRequest,
    res: NextApiResponse<Data>) {
        if (req.query.collection) {
            if (Number(req.query.time) === -1) {
                let data = await getLatest(req.query.collection as string);
                if (!data) {
                    console.log(`Request with collection ${req.query.collection} and time ${req.query.time} returned no data!`);
                }
                return res.status(200).json({sim_data : data})
            } else if (Number(req.query.time) >= 0) {
                let data = await getSpecific(req.query.collection as string, Number(req.query.time));
                if (!data) {
                    console.log(`Request with collection '${req.query.collection}' and time '${req.query.time}' (${typeof Number(req.query.time)}) returned no data!`);
                }
                return res.status(200).json({sim_data : data});
            } else {
                console.log("Invalid time was given!")
            }
        } else {
            console.log("No collection name was given!");
        }
}