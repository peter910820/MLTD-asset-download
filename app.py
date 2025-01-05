import asyncio

from src.tool import AssetDownload

if __name__ == "__main__":
    asset_download = AssetDownload()
    asyncio.run(asset_download.main())
