SELECT
    GRID.reporting_ts,
    SOLAR.lifetime_energy AS total_solar_energy,
    coalesce(SOLAR.solar_energy,0,SOLAR.solar_energy) AS solar_energy_generated_since_last_poll,
    SOLAR.power AS solar_power_reading_kw,
    GRID.lifetime_energy AS total_grid_energy,
    GRID.grid_energy AS grid_energy_used_since_last_poll,
    GRID.power AS grid_power_reading_kw,
    SOLAR.lifetime_energy+GRID.lifetime_energy AS total_home_consumption,
    coalesce(SOLAR.solar_energy,0,SOLAR.solar_energy)+GRID.grid_energy AS home_consumption_since_last_poll
FROM
(SELECT
  reporting_ts,
  CAST (data_payload->>'net_ltea_3phsum_kwh' AS float) AS lifetime_energy,
  CAST (data_payload->>'net_ltea_3phsum_kwh' AS float) - LAG(CAST (data_payload->>'net_ltea_3phsum_kwh' AS float)) OVER (ORDER BY reporting_ts) AS solar_energy,
  CAST (data_payload->>'p_3phsum_kw' AS float) AS power
FROM
  solar_generation
WHERE
  DEVICE_TYPE = 'PVS5-METER-P') SOLAR
INNER JOIN
(SELECT
  reporting_ts,
  CAST (data_payload->>'net_ltea_3phsum_kwh' AS float) AS lifetime_energy,
  CAST (data_payload->>'net_ltea_3phsum_kwh' AS float) - LAG(CAST (data_payload->>'net_ltea_3phsum_kwh' AS float)) OVER (ORDER BY reporting_ts) AS grid_energy,
  CAST (data_payload->>'p_3phsum_kw' AS float) AS power
FROM
  solar_generation
WHERE
  DEVICE_TYPE = 'PVS5-METER-C'
ORDER BY reporting_ts ASC) GRID
ON (SOLAR.reporting_ts = GRID.reporting_ts)
ORDER BY GRID.reporting_ts ASC;