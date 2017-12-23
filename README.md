Global Settlement of Sai occured today, Friday 22nd, at 0115 UTC, at an ETH
price of $779.018

https://etherscan.io/tx/0xf3582ee20b92474a4cd03b27a096bd9b6963809b054bc6f363a3cf97fef63446

- All Sai holders can now cash their Sai for WETH, fixed at 0.00128 WETH per Sai
- All CDP owners can recover their collateral, by first freeing their
  SKR and then exiting their SKR into WETH.
- SKR holders can just exit into WETH.

A bug was discovered in the settlement process three weeks ago, in the final
audit of the Dai code. The bug is that the liquidation penalty should be set
to 0% on settlement, but this was not applied and instead remained at 20%.
This bug has been fixed in Dai.


## Technical details

Normally it is only possible to `bite` (liquidate) an unsafe CDP. After
`cage`, it is possible to `bite` any CDP. This allows for system state
to be wound down and the appropriate value of the SKR collateral to be
determined.

The following assumptions are made:

1. No tokens in the `tap`.
2. All CDPs well collateralised
3. All unlocked SKR aggregated into a single CDP

And the terms used here have the following meaning:

- `tab`: CDP debt
- `ink`: CDP collateral (SKR)
- `ice`: Total CDP debt
- `air`: Total CDP collateral
- `pie`: Total ETH base collateral
- `per`: ETH per SKR ratio for `exit`
- `tag`: USD price of SKR
- `axe`: Liquidation penalty (multiplicative, 1 is 0%, 1.2 is 20%)


Following `bite`, the SKR remaining in a CDP is given by

```
ink' = ink - (tab * axe) / tag
```

Similarly, following `cage`, the SKR remaining in the system is given by

```
air' = air - (ice * axe) / tag
```

and the ETH collateral remaining is given by

```
pie' = pie - ice / (tag / per)
```

The new value of `per` is given by

```
per' = pie' / air'
```

It follows that the amount of ETH that a CDP owner can exit with is given by

```
exit = ink' * per'
exit = pie' * (ink * tag - tab * axe) / (air * tag - ice * axe)
```

We can then compute the difference in ETH between what a CDP owner can
`exit` with and what they *should* have been able to `exit` with.

```
diff = tag * pie' * (axe1 - axe0) (ink*ice - air*tab) / [ (air*tag - ice*axe0) (air*tag - ice*axe1) ]
```

`cups.json` contains a listing of all CDPs in the system immediately
before `cage`. All SKR that wasn't locked in a CDP was aggregated into
CDP 255, with zero debt, for ease of calculation. This data can be
regenerated with `./getcups > cups.json`.

The loss calculation can be performed with `python cage.py`. The output
shows the non-zero value CDPs and their associated loss `-` or gain `+`.
This process is zero sum: the total CDP loss should equal the total CDP
gain.
