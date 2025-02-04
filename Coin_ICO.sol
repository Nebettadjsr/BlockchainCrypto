// SPDX-License-Identifier: MIT
// Coin ICO Smart Contract for Network
// example Coin = Bcoin


// Version of Compiler
pragma solidity ^0.8.26;

contract coin_ico {
    // Max Number of Coins for Sale:
    uint public max_Bcoin = 1000000;

    // introducing USD - Coin conversion rate
    uint public usd_to_Bcoin = 1000;

    // introducing total number of coin bought by investors
    uint public total_Bcoin_bought = 0;

    //Mapping investor address to equidity in Coin and USD
    mapping(address => uint) equity_in_Bcoin;
    mapping(address => uint) equity_in_USD;

    //Chek if investor can by coin
    modifier can_buy_Bcoin(uint usd_invested){
        require(usd_invested * usd_to_Bcoin + total_Bcoin_bought <= max_Bcoin);
        _;
    }

    // Getting equity in Coin of Investor
    function equity_in_coin(address investor) external view returns (uint) {
        return equity_in_Bcoin[investor];
    }

    // Getting equity in USD of Investor
    function equity_in_usd(address investor) external view returns (uint) {
        return equity_in_USD[investor];
    }

    //Buying coin
    function buy_coin(address investor, uint usd_invested) external 
    can_buy_Bcoin(usd_invested) {
        uint coins_bought = usd_invested * usd_to_Bcoin;
        equity_in_Bcoin[investor] += coins_bought;
        equity_in_USD[investor] = equity_in_Bcoin[investor] / 1000;
        total_Bcoin_bought += coins_bought;
    }

    // Sell Coin
    function sell_coin(address investor, uint coin_for_sell) external {        
        equity_in_Bcoin[investor] -= coin_for_sell;
        equity_in_USD[investor] = equity_in_Bcoin[investor] / 1000;
        total_Bcoin_bought -= coin_for_sell;
    }
}
