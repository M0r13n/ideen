# 3339 - Date and Time on the Internet

[RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339#section-4) specifies a date and time format that is commonly used in internet protocols and applications. The format is based on the ISO 8601 standard and represents dates and times in a consistent and unambiguous way. Here are some examples of date and time values formatted according to RFC 3339:

1. Date and Time in Coordinated Universal Time (UTC):
    - 2023-07-22T12:34:56Z
    - 2023-12-31T23:59:59Z
2. Date and Time with Timezone Offset:
    - 2023-07-22T12:34:56+00:00
    - 2023-07-22T12:34:56-05:00
    - 2023-07-22T12:34:56+02:00
3. Date Only:
    - 2023-07-22
4. Date and Time with Fractional Seconds:
    - 2023-07-22T12:34:56.123Z
    - 2023-07-22T12:34:56.54321Z

Remember, the 'Z' at the end of the string indicates that the time is in UTC (Coordinated Universal Time). If there is a timezone offset included, it will be represented as '+HH:MM' or '-HH:MM' after the time portion. Also, note that RFC 3339 allows fractional seconds for higher precision if necessary.

## Restrictions

Month Number  Month/Year           Maximum value of date-mday
  ------------  ----------           --------------------------
  01            January              31
  02            February, normal     28
  02            February, leap year  29
  03            March                31
  04            April                30
  05            May                  31
  06            June                 30
  07            July                 31
  08            August               31
  09            September            30
  10            October              31
  11            November             30
  12            December             31