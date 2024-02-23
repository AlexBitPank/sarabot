import sys
import aiomysql


async def create_pool():
    global pool
    try:
        # pool = await aiomysql.create_pool(host="localhost", port=3306,
        #                             user="root", password="",
        #                             db="u2229695_default", autocommit=True)
        pool = await aiomysql.create_pool(host="sarahr.ru", port=3306,
                                    user="u2229695_default", password="qHs2xI8GN2rXogN5",
                                    db="u2229695_default", autocommit=True)
        print('Подключились к БД...')
        # return pool
    except Exception:
        print('Failed to connect to database')
        sys.exit()

async def select(query):
    global pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:    
            await cursor.execute(query)
            records = await cursor.fetchall()
            return records

async def insert(query):
    global pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:    
            await cursor.execute(query)

async def get_listings():
    query = f"""SELECT
                `ID`,
                `post_title`,
                `post_content`,
                `post_excerpt`
            FROM
                `wp_posts`
            WHERE
                `post_type` = 'hp_listing' AND `post_status` = 'publish'
            ORDER BY
                `wp_posts`.`post_title`
            ASC
            """
    records = await select(query)
    return records

async def get_limit_listings(limit = 5):
    query = f"""SELECT
                    `ID`,
                    `post_title`,
                    `post_content`,
                    `post_excerpt`,
                    `wp_postmeta`.`meta_value`
                FROM
                    `wp_posts`
                JOIN `wp_postmeta` ON `wp_postmeta`.`post_id` = `wp_posts`.`ID`
                WHERE
                    `wp_postmeta`.`meta_key` = 'hp_number' AND `wp_posts`.`post_type` = 'hp_listing' AND `wp_posts`.`post_status` = 'publish'
                ORDER BY
                    `wp_posts`.`post_modified`
                DESC
                LIMIT {limit}
            """
    records = await select(query)
    return records

async def get_listing_by_number(number):
    query = f"""
            SELECT
                `wp_posts`.`ID`,
                `wp_posts`.`post_title`,
                `wp_posts`.`post_content`,
                `wp_posts`.`post_excerpt`
            FROM
                `wp_posts`
            JOIN `wp_postmeta` ON `wp_postmeta`.`post_id` = wp_posts.ID
            WHERE
                `wp_postmeta`.`meta_key` = 'hp_number' AND `wp_postmeta`.`meta_value` = {number} AND `wp_posts`.`post_type` = 'hp_listing' AND `wp_posts`.`post_status` = 'publish'
            """
    records = await select(query)
    return records

async def get_listing_attribute(id):
    query = f"""SELECT REPLACE(`meta_key`, 'hp_', ''), `meta_value`
                    FROM `wp_postmeta`
                    WHERE `post_id` = {id} AND `meta_key` LIKE 'hp_%'
                    UNION ALL
                    SELECT REPLACE(`wp_term_taxonomy`.`taxonomy`, 'hp_listing_', '') AS `meta_key`, `wp_terms`.`name` AS `meta_value`
                    FROM `wp_term_relationships`
                    JOIN `wp_terms` ON `wp_term_relationships`.`term_taxonomy_id` = `wp_terms`.`term_id`
                    JOIN `wp_term_taxonomy` ON `wp_terms`.`term_id`= `wp_term_taxonomy`.`term_id`
                    WHERE `wp_term_relationships`.`object_id` = {id};
            """
    records = await select(query)
    return {str(record[0]): str(record[1]) for record in records}