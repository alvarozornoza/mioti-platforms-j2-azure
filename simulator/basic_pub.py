# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
import random
import logging
import json
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient

async def main():
    # Fetch the connection string from an environment variable
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope = ""
    registration_id = ""
    symmetric_key = ""
    model_id = "test"

    registration_result = await provision_device(
        provisioning_host, id_scope, registration_id, symmetric_key, model_id
    )

    if registration_result.status == "assigned":
        print("Device was assigned")
        print(registration_result.registration_state.assigned_hub)
        print(registration_result.registration_state.device_id)

        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
    else:
        raise RuntimeError(
            "Could not provision device. Aborting Plug and Play device connection."
        )

    # Connect the device client.
    await device_client.connect()

    ################################################
    # Send telemetry (current temperature)

    async def send_telemetry():
        print("Sending telemetry")

        while True:
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 50), 2)
            telemetry_msg = {"temperature": temperature, "humidity": humidity}
            msg = json.dumps(telemetry_msg)
            print("Sent message", msg)
            await device_client.send_message(msg)
            await asyncio.sleep(5)

    send_telemetry_task = asyncio.create_task(send_telemetry())

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    # # Wait for user to indicate they are done listening for method calls
    await user_finished

    send_telemetry_task.cancel()

    # Finally, shut down the client
    await device_client.shutdown()

#####################################################
# An # END KEYBOARD INPUT LISTENER to quit application
def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break

#####################################################
# PROVISION DEVICE
async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )
    return await provisioning_device_client.register()


if __name__ == "__main__":
    asyncio.run(main())

# If using Python 3.6 use the following code instead of asyncio.run(main()):
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
