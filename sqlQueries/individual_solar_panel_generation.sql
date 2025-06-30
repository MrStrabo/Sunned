SELECT
  reporting_ts, SERIAL_NUMBER,
  CAST (data_payload->>'ltea_3phsum_kwh' AS float) AS lifetime_energy_kwh,
  CAST (data_payload->>'p_3phsum_kw' AS float) AS power_kw
FROM
  solar_generation
WHERE
  DEVICE_TYPE = 'SOLARBRIDGE'
ORDER BY
    reporting_ts ASC;
