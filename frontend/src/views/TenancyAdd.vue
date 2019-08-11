<template>
<div id="tenancy-new">
  <div class="tenant-names">
    <div class="table-container">
      <table class="table tenant-list">
        <thead>
          <th scope="col">Tenant Name</th>
          <th scope="col"></th>
        </thead>
        <tbody>
          <tr v-for="tenantField in tenantNames.tenantFields" v-bind:key="tenantField.name">
            <td>
              <input type="text" v-model="tenantField.value" v-bind:name="tenantField.name">
            </td>
            <td>
              <div class="btn btn-normal" v-on:click="deleteTenant(tenantField.name)">
                Delete
              </div>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <div class="btn btn-normal" v-on:click="addTenant()">
            Add Tenant
          </div>
        </tfoot>
      </table>
    </div>
  </div>
  <div class="date-range">
    <div class="start-date">
      <label>Start Date:</label>
      <input type="text" v-model="dateRange.startDate">
    </div>
    <div class="end-date">
      <label>End Date:</label>
      <input type="text" v-model="dateRange.endDate">
    </div>
  </div>
  <div class="rent-payment">
    <div>
      <label>Payment Terms:</label>
    </div>
    <div>
      <select v-on:change="paymentTermsChange($event)">
        <option value="0" selected="selected" disabled>
          -- Please select your payment terms --
        </option>
        <option v-for="paymentTerms in rentPayment.paymentTermsList"
        v-bind:key="paymentTerms.name" v-bind:value="paymentTerms.value">
          {{ paymentTerms.value }}
        </option>
      </select>
    </div>
    <div>
      <label>Rent Cost (AUD):</label>
    </div>
    <div>
      $ <input type="number" v-model="rentPayment.rentCost">&nbsp;
      <label v-if="rentPayment.selectedRentPayment != '0'">
        {{ rentPayment.selectedRentPayment }}
      </label>
    </div>
    <div>
      <label>Payment Method Description:</label>
    </div>
    <div>
      <textarea v-model="rentPayment.paymentDescription"></textarea>
    </div>
  </div>
  <div class="property-details">
    <div>
      <label>Property Address:</label>
    </div>
    <div>
      <input type="text" v-model="propertyDetails.propertyAddress">
    </div>
    <div>
      <label>Rent Type:</label>
    </div>
    <div>
      <select v-on:change="rentTypeChange($event)">
        <option value="0" selected="selected" disabled>
          -- Please select a rent type --
        </option>
        <option v-for="rentType in propertyDetails.rentTypeList"
        v-bind:key="rentType.name" v-bind:value="rentType.value">
          {{ rentType.value }}
        </option>
      </select>
    </div>
    <div>
      <label>Room Name:</label>
    </div>
    <div>
      <input type="text" v-model="propertyDetails.roomName">
    </div>
  </div>
  <div class="notification-scheduling">
    <div class="table-container">
      <table class="table notification-list">
        <thead>
          <th>
            Notifications
          </th>
          <th>
            Days in advance of rent due date
          </th>
          <th>
          </th>
        </thead>
        <tbody>
          <tr v-for="notification in notifications.notificationFields"
          v-bind:key="notification.name">
            <td>
              Notification {{ notification.name }}
            </td>
            <td>
              <select v-on:change="notificationChange($event, notification.name)"
              v-bind:value="notification.value">
                <option v-for="day in notifications.days" v-bind:key="day">{{ day }}</option>
              </select>
            </td>
            <td></td>
          </tr>
        </tbody>
        <tfoot>
          <div class="btn" v-on:click="addNotification()">Add Nofication Schedule</div>
        </tfoot>
      </table>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'tenancy-new',
  data() {
    return {
      tenantNames: {
        tenantFields: [],
        tenantFieldIndex: 0,
      },
      dateRange: {
        startDate: '',
        endDate: '',
      },
      rentPayment: {
        paymentTermsList: [
          { name: 'Per week', value: 'Per week' },
          { name: 'Per fortnight', value: 'Per fortnight' },
          { name: 'Per month', value: 'Per month' },
        ],
        selectedRentPayment: '0',
        paymentDescription: '',
      },
      propertyDetails: {
        propertyAddress: '',
        rentTypeList: [
          { name: 'Whole Property', value: 'Whole Property' },
          { name: 'Private Room', value: 'Private Room' },
        ],
        roomName: '',
      },
      notifications: {
        notificationFields: [],
        notificationFieldIndex: 0,
        days: Array(14).fill().map((_, i) => i + 1),
      },
    };
  },
  methods: {
    addTenant() {
      this.tenantNames.tenantFields.push({
        name: this.tenantNames.tenantFieldIndex,
        value: '',
      });
      this.tenantNames.tenantFieldIndex += 1;
    },
    deleteTenant(name) {
      this.tenantNames.tenantFields = this.tenantNames.tenantFields.filter(
        tenantField => tenantField.name !== name,
      );
    },
    paymentTermsChange(event) {
      this.rentPayment.selectedRentPayment = event.target.value;
    },
    paymentMethodChange(event) {
      this.rentPayment.selectedPaymentMethod = event.target.value;
    },
    addNotification() {
      this.notifications.notificationFields.push({
        name: this.notifications.notificationFieldIndex,
        value: 7,
      });
      this.notifications.notificationFieldIndex += 1;
    },
    notificationChange(event, notificationFieldName) {
      this.notifications.notificationFields.find(
        notification => notification.name === notificationFieldName,
      ).value = parseInt(event.target.value);
    },
  },
};
</script>
