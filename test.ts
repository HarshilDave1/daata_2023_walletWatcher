import { CovalentClient } from "@covalenthq/client-sdk";

const ApiServices = async () => {
    const client = new CovalentClient("cqt_rQBk7jfGvkByY7TqQBqbHfrBJKKf");
    try {
        for await (const resp of client.TransactionService.getAllTransactionsForAddress("eth-mainnet","0x6e19Fc0Ce57081420CA1f60F5eBe46b2c55CC5E0", {})) {
            console.log(resp);
        }
    } catch (error) {
        console.log(error.message);
    }
}
